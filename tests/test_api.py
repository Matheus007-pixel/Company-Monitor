import pytest
from fastapi.testclient import TestClient

import api
from api import app

client = TestClient(app)

CHAVE = "chave-de-teste"

MEDICAO = {
    "computador": "PC-TESTE",
    "cpu": 50,
    "ram": 95,
    "disco": 50,
    "internet": True,
}


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


def test_historico(monkeypatch):
    def historico_falso():
        return [
            {
                "data_hora": "25/10/2026 20:00:00",
                "computador": "PC-TESTE",
                "cpu": "50.0",
                "ram": "60.0",
                "disco": "40.0",
                "internet": "True",
                "status_geral": "OK",
            }
        ]

    monkeypatch.setattr(api, "ler_historico", historico_falso)

    resposta = client.get("/historico")
    dados = resposta.json()

    assert resposta.status_code == 200
    assert len(dados) == 1
    assert dados[0]["computador"] == "PC-TESTE"
    assert dados[0]["status_geral"] == "OK"


@pytest.fixture
def registros(monkeypatch):
    """Configura a chave e troca a gravação no banco por uma versão falsa."""
    monkeypatch.setenv("API_KEY", CHAVE)
    chamadas = []

    def registrar_falso(informacoes, status_geral):
        chamadas.append((informacoes, status_geral))

    monkeypatch.setattr(api, "registrar_medicao", registrar_falso)
    return chamadas


def test_medicao_com_chave_certa_grava(registros):
    resposta = client.post("/medicoes", json=MEDICAO, headers={"X-API-Key": CHAVE})

    assert resposta.status_code == 201
    assert resposta.json() == {
        "status": "registrada",
        "computador": "PC-TESTE",
        "status_geral": "CRÍTICO",
    }
    assert len(registros) == 1
    informacoes, status_geral = registros[0]
    assert informacoes["computador"] == "PC-TESTE"
    assert informacoes["ram"] == 95
    assert informacoes["internet"] is True
    assert status_geral == "CRÍTICO"


def test_medicao_com_chave_errada_e_recusada(registros):
    resposta = client.post("/medicoes", json=MEDICAO, headers={"X-API-Key": "errada"})

    assert resposta.status_code == 401
    assert registros == []


def test_medicao_sem_chave_e_recusada(registros):
    resposta = client.post("/medicoes", json=MEDICAO)

    assert resposta.status_code == 401
    assert registros == []


def test_medicao_sem_api_key_configurada_e_recusada(registros, monkeypatch):
    monkeypatch.delenv("API_KEY")

    resposta = client.post("/medicoes", json=MEDICAO, headers={"X-API-Key": CHAVE})

    assert resposta.status_code == 503
    assert registros == []


def test_medicao_com_valor_invalido_e_recusada(registros):
    invalida = {**MEDICAO, "cpu": 150}

    resposta = client.post("/medicoes", json=invalida, headers={"X-API-Key": CHAVE})

    assert resposta.status_code == 422
    assert registros == []


def test_medicao_com_campo_faltando_e_recusada(registros):
    incompleta = {k: v for k, v in MEDICAO.items() if k != "disco"}

    resposta = client.post("/medicoes", json=incompleta, headers={"X-API-Key": CHAVE})

    assert resposta.status_code == 422
    assert registros == []