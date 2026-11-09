"""API mínima do Encosta Viva (versão simples para a entrega de Cloud).

Endpoints:
  GET  /saude                    -> health check
  POST /leituras                 -> recebe a leitura do robô (precisa do header X-API-Key)
  GET  /setores/{id}/risco       -> último nível do setor e o porquê
  GET  /metrics                  -> métricas para o Prometheus
"""
import os
import secrets
import time

import httpx
from fastapi import FastAPI, Header, HTTPException
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field

# Configuração só por variável de ambiente (nunca no código).
API_KEY = os.getenv("API_KEY", "")
# Opcional: endpoint do assistente (GenAI) do grupo, ex.: https://.../assistente/perguntar
ASSISTENTE_URL = os.getenv("ASSISTENTE_URL", "")

app = FastAPI(title="Encosta Viva API", version="0.1.0")
LEITURAS = Counter("leituras", "Leituras de sensor recebidas")  # exposto como leituras_total

FRASES = {
    "NORMAL": "Solo estável. Sem alerta no momento.",
    "ATENCAO": "Solo ficando encharcado. Observe rachaduras e portas que emperram.",
    "ALERTA": "Solo muito encharcado. Se as rachaduras aumentarem, saia de casa. Em emergência, ligue 199 ou 193.",
    "ERRO": "Sensor com falha. Leitura indisponível neste momento.",
}

# Estado em memória (suficiente para o MVP; sem dado pessoal, só setor e leitura).
ULTIMA: dict[str, dict] = {}


class Leitura(BaseModel):
    setor_id: str = Field(min_length=1, max_length=50)
    umidade_pct: float = Field(ge=0, le=100)
    nivel: str = Field(pattern=r"^(NORMAL|ATENCAO|ALERTA|ERRO)$")


def _gerar_frase(leitura: Leitura) -> str:
    """Frase de orientação. Usa o assistente (LLM) se configurado; senão, frase fixa."""
    padrao = FRASES[leitura.nivel]
    if not ASSISTENTE_URL:
        return padrao
    pergunta = (
        f"Setor {leitura.setor_id}, umidade do solo {leitura.umidade_pct:.0f}%, "
        f"nível {leitura.nivel}. Responda em uma frase simples orientando o morador. "
        "Não decida evacuação."
    )
    try:
        resp = httpx.post(ASSISTENTE_URL, json={"pergunta": pergunta}, timeout=5)
        resp.raise_for_status()
        return resp.json().get("resposta") or padrao
    except Exception:
        return padrao  # se o assistente falhar, o robô continua recebendo orientação


@app.get("/saude")
def saude():
    return {"status": "ok"}


@app.post("/leituras")
def receber_leitura(leitura: Leitura, x_api_key: str | None = Header(default=None)):
    if not API_KEY or not x_api_key or not secrets.compare_digest(
        x_api_key.encode(), API_KEY.encode()
    ):
        raise HTTPException(status_code=401, detail="chave inválida")

    anterior = ULTIMA.get(leitura.setor_id)
    mudou = anterior is None or anterior["nivel"] != leitura.nivel
    # Só chama o assistente quando o nível muda (evita sobrecarga e latência).
    frase = _gerar_frase(leitura) if mudou else anterior["frase"]

    ULTIMA[leitura.setor_id] = {
        "nivel": leitura.nivel,
        "umidade_pct": leitura.umidade_pct,
        "frase": frase,
        "recebido_em": time.time(),
    }
    LEITURAS.inc()
    return {"frase": frase}


@app.get("/setores/{setor_id}/risco")
def risco(setor_id: str):
    dado = ULTIMA.get(setor_id)
    if dado is None:
        raise HTTPException(status_code=404, detail="sem leituras para este setor")
    return {
        "setor_id": setor_id,
        "nivel": dado["nivel"],
        "porque": f"umidade do solo em {dado['umidade_pct']:.0f}%",
        "frase": dado["frase"],
        "atualizado_em": dado["recebido_em"],
    }


# Expõe /metrics (latência, tráfego, erros) para Prometheus/Grafana.
Instrumentator().instrument(app).expose(app)
