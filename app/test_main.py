import os

os.environ["API_KEY"] = "chave-teste"  # antes de importar o app

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402

client = TestClient(app)
HEADERS = {"X-API-Key": "chave-teste"}
LEITURA = {"setor_id": "vila-sahy", "umidade_pct": 82, "nivel": "ALERTA"}


def test_saude():
    r = client.get("/saude")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_leitura_sem_chave_e_negada():
    assert client.post("/leituras", json=LEITURA).status_code == 401


def test_leitura_invalida_e_rejeitada():
    ruim = {**LEITURA, "umidade_pct": 150}
    assert client.post("/leituras", json=ruim, headers=HEADERS).status_code == 422


def test_leitura_ok_e_risco():
    r = client.post("/leituras", json=LEITURA, headers=HEADERS)
    assert r.status_code == 200
    assert "frase" in r.json()
    risco = client.get("/setores/vila-sahy/risco")
    assert risco.status_code == 200
    assert risco.json()["nivel"] == "ALERTA"


def test_risco_de_setor_sem_leitura():
    assert client.get("/setores/nao-existe/risco").status_code == 404
