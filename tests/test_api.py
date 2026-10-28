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

def test_processos(monkeypatch):
    def processos_falsos():
        return [
            {"nome": "chrome.exe", "memoria": 25.0, "memoria_mb": 4000.0, "quantidade": 12},
            {"nome": "code.exe", "memoria": 5.0, "memoria_mb": 800.0, "quantidade": 3},
        ]

    monkeypatch.setattr(api, "obter_processos", processos_falsos)

    resposta = client.get("/processos")
    dados = resposta.json()

    assert resposta.status_code == 200
    assert dados["status"] == "CRÍTICO"
    assert "chrome.exe" in dados["mensagem"]
    assert len(dados["processos"]) == 2
    assert dados["processos"][0]["nome"] == "chrome.exe"