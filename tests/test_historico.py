from datetime import datetime

import pytest

from historico import (
    FORMATO_DATA,
    _conectar,
    _criar_tabela,
    ler_historico,
    registrar_medicao,
)

INFORMACOES = {
    "computador": "PC-TESTE",
    "cpu": 12.5,
    "ram": 45.0,
    "disco": 60.0,
    "internet": True,
}


@pytest.fixture(autouse=True)
def banco_de_teste(monkeypatch):
    monkeypatch.setenv("DB_NAME", "company_monitor_test")

    with _conectar() as conexao:
        banco = conexao.execute("SELECT current_database()").fetchone()[0]
        assert banco == "company_monitor_test", f"Banco inesperado: {banco}"
        _criar_tabela(conexao)
        conexao.execute("TRUNCATE TABLE historico RESTART IDENTITY")

    yield


def test_historico_vazio_devolve_lista_vazia():
    assert ler_historico() == []


def test_registrar_e_ler_devolve_as_colunas_esperadas():
    registrar_medicao(INFORMACOES, "OK")

    medicoes = ler_historico()

    assert len(medicoes) == 1
    assert list(medicoes[0].keys()) == [
        "data_hora",
        "computador",
        "cpu",
        "ram",
        "disco",
        "internet",
        "status_geral",
    ]


def test_valores_voltam_como_texto():
    registrar_medicao(INFORMACOES, "OK")

    medicao = ler_historico()[0]

    assert medicao["computador"] == "PC-TESTE"
    assert medicao["cpu"] == "12.5"
    assert medicao["internet"] == "True"
    assert medicao["status_geral"] == "OK"


def test_data_hora_volta_no_formato_brasileiro():
    registrar_medicao(INFORMACOES, "OK")

    medicao = ler_historico()[0]

    datetime.strptime(medicao["data_hora"], FORMATO_DATA)


def test_medicoes_voltam_em_ordem_de_registro():
    registrar_medicao(INFORMACOES, "OK")
    registrar_medicao(INFORMACOES, "ATENÇÃO")

    status = [m["status_geral"] for m in ler_historico()]

    assert status == ["OK", "ATENÇÃO"]