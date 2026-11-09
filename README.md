# Encosta Viva

Alerta antecipado de deslizamento para comunidades que vivem em áreas de risco.
Entrega de **Secure DevOps Tools & Cloud Computing** · FIAP Global Solution 2026.2 · CitizenTech · 4ES.

## Integrantes

| Nome completo | RM |
|---|---|
| Ricardo Matos | 95906 |
| (preencher) | (preencher) |
| (preencher) | (preencher) |

## Ficha Técnica do MVP

| Campo | Descrição |
|---|---|
| Nome do produto | Encosta Viva |
| Cidadão e território | Moradores de setores de risco alto e muito alto (R3/R4) em encostas urbanas (periferias da Grande SP, Litoral Norte, Petrópolis) e o agente da Defesa Civil municipal que monitora essas áreas. |
| Problema, em uma frase | Quem mora em encosta recebe alertas genéricos por município, tarde demais e sem saber o que fazer, enquanto a Defesa Civil não tem olhos no terreno entre uma vistoria e outra. |
| Proposta de valor | Alerta por setor de risco (não por cidade), combinando chuva, umidade e movimento do solo, com orientação clara em linguagem simples e funcionando mesmo sem internet no local. |
| Arquitetura: componentes | Robô sentinela (ESP32) · API FastAPI em container · Azure Container Apps · pipeline GitHub Actions (DevSecOps) · Prometheus + Grafana · Terraform |
| Fontes de dados | Leituras de umidade do solo do robô sentinela; Open-Meteo (chuva); CEMADEN; IBGE |
| Modelos de IA utilizados | Assistente (LLM local) que gera a frase de orientação, chamado pela API quando o nível muda |
| URL do MVP e repositório | MVP: (colar a URL do output do Terraform) · Repositório: (colar o link do GitHub) |
| Indicadores de impacto | Minutos de antecedência do alerta · leituras recebidas por minuto · uptime da API · falsos alarmes por mês |
| ODS conectados | 11 (meta 11.5) · 13 (meta 13.1) · 9 · 10 · 3 |

## O que tem neste repositório

```
app/                  API FastAPI (main.py) + testes (pytest)
Dockerfile            multi-stage, imagem slim, usuário não root, sem segredo
docker-compose.yml    api + prometheus + grafana
monitoring/           prometheus.yml, alerts.yml e dashboard do Grafana (4 sinais de ouro)
infra/                Terraform (Azure Container Apps)
.github/workflows/    pipeline: pytest -> Gitleaks -> Semgrep -> Trivy -> GHCR -> deploy
docs/                 ARQUITETURA.md e PUBLICAR.md (passo a passo)
```

## Rodar localmente

```powershell
Copy-Item .env.example .env      # preencha API_KEY e GRAFANA_PASSWORD no .env
docker compose up --build
```

| Serviço | Endereço |
|---|---|
| API | http://localhost:8000 (docs em `/docs`) |
| Prometheus | http://localhost:9090 (alertas em `/alerts`) |
| Grafana | http://localhost:3000 (usuário `admin`, senha = `GRAFANA_PASSWORD`) |

## Contrato da API (usado pelo robô e pelo app)

| Método | Rota | O que faz |
|---|---|---|
| GET | `/saude` | health check |
| POST | `/leituras` | recebe `{"setor_id","umidade_pct","nivel"}` com o header `X-API-Key`; devolve `{"frase"}` |
| GET | `/setores/{id}/risco` | último nível do setor e o porquê |
| GET | `/metrics` | métricas Prometheus |

`nivel` aceita: `NORMAL`, `ATENCAO`, `ALERTA`, `ERRO`.

## Segurança e LGPD

- Nenhum segredo no código ou na imagem: a chave da API vem de variável de ambiente (Secret do Container App).
- `terraform.tfstate`, `*.tfvars` e `.env` estão no `.gitignore`.
- A API não guarda dado pessoal: só setor, umidade e nível.
- A IA não decide evacuação: o nível vem da regra do robô e quem decide remover pessoas é a Defesa Civil.
