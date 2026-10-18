import pytest

from analise import (
    analisar_cpu,
    analisar_ram,
    analisar_disco,
    analisar_internet,
    analisar_computador,
    obter_status_geral,
    analisar_processos,
)


@pytest.mark.parametrize("uso, esperado", [
    (None, "INDISPONÍVEL"),
    (0, "OK"),
    (69.9, "OK"),
    (70, "ATENÇÃO"),
    (89.9, "ATENÇÃO"),
    (90, "CRÍTICO"),
    (100, "CRÍTICO"),
])
def test_analisar_cpu(uso, esperado):
    assert analisar_cpu(uso)["status"] == esperado


@pytest.mark.parametrize("uso, esperado", [
    (None, "INDISPONÍVEL"),
    (0, "OK"),
    (69.9, "OK"),
    (70, "ATENÇÃO"),
    (89.9, "ATENÇÃO"),
    (90, "CRÍTICO"),
    (100, "CRÍTICO"),
])
def test_analisar_ram(uso, esperado):
    assert analisar_ram(uso)["status"] == esperado


@pytest.mark.parametrize("uso, esperado", [
    (None, "INDISPONÍVEL"),
    (0, "OK"),
    (74.9, "OK"),
    (75, "ATENÇÃO"),
    (89.9, "ATENÇÃO"),
    (90, "CRÍTICO"),
    (100, "CRÍTICO"),
])
def test_analisar_disco(uso, esperado):
    assert analisar_disco(uso)["status"] == esperado


def test_analisar_internet_conectada():
    assert analisar_internet(True)["status"] == "OK"


def test_analisar_internet_desconectada():
    assert analisar_internet(False)["status"] == "CRÍTICO"


def test_analisar_computador_retorna_os_quatro_recursos():
    resultado = analisar_computador(cpu=50, ram=80, disco=95, internet=True)

    assert set(resultado) == {"cpu", "ram", "disco", "internet"}
    assert resultado["cpu"]["status"] == "OK"
    assert resultado["ram"]["status"] == "ATENÇÃO"
    assert resultado["disco"]["status"] == "CRÍTICO"
    assert resultado["internet"]["status"] == "OK"


def montar_analise(cpu="OK", ram="OK", disco="OK", internet="OK"):
    return {
        "cpu": {"status": cpu},
        "ram": {"status": ram},
        "disco": {"status": disco},
        "internet": {"status": internet},
    }


def test_status_geral_tudo_ok():
    assert obter_status_geral(montar_analise()) == "OK"


def test_status_geral_com_atencao():
    assert obter_status_geral(montar_analise(ram="ATENÇÃO")) == "ATENÇÃO"


def test_status_geral_critico_vence_atencao():
    analise = montar_analise(cpu="ATENÇÃO", disco="CRÍTICO")
    assert obter_status_geral(analise) == "CRÍTICO"


def test_processos_lista_vazia():
    resultado = analisar_processos([])

    assert resultado["status"] == "OK"
    assert resultado["processos"] == []


@pytest.mark.parametrize("memoria, esperado", [
    (9.9, "OK"),
    (10, "ATENÇÃO"),
    (19.9, "ATENÇÃO"),
    (20, "CRÍTICO"),
])
def test_processos_limites_de_memoria(memoria, esperado):
    processos = [{"nome": "chrome.exe", "memoria": memoria}]

    assert analisar_processos(processos)["status"] == esperado


def test_processos_mensagem_cita_o_maior_processo():
    processos = [
        {"nome": "chrome.exe", "memoria": 25.0},
        {"nome": "code.exe", "memoria": 5.0},
    ]

    resultado = analisar_processos(processos)

    assert "chrome.exe" in resultado["mensagem"]

def test_status_geral_indisponivel_nao_vira_ok():
    assert obter_status_geral(montar_analise(cpu="INDISPONÍVEL")) == "ATENÇÃO"


def test_status_geral_critico_vence_indisponivel():
    analise = montar_analise(cpu="INDISPONÍVEL", disco="CRÍTICO")
    assert obter_status_geral(analise) == "CRÍTICO"