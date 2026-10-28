from fastapi.testclient import TestClient

import api
from api import app
client = TestClient(app)


def test_saude():
    resposta = client.get("/saude")

    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}

def test_status(monkeypatch):
    def informacoes_falsas():
        return {
            "cpu": 50,
            "ram": 95,
            "disco": 50,
            "internet": True,
            "computador": "PC-TESTE",
            "uptime": "1 horas, 0 minutos",
            "sistema": "Windows",
            "processos": [],
        }

    monkeypatch.setattr(api, "coletar_informacoes", informacoes_falsas)

    resposta = client.get("/status")
    dados = resposta.json()

    assert resposta.status_code == 200
    assert dados["computador"] == "PC-TESTE"
    assert dados["cpu"] == 50
    assert dados["analise"]["cpu"]["status"] == "OK"
    assert dados["analise"]["ram"]["status"] == "CRÍTICO"
    assert dados["status_geral"] == "CRÍTICO"