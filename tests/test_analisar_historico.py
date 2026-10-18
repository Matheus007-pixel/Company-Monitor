import pytest

from analise import analisar_historico

CHAVES = {
    "quantidade", "cpu_media", "ram_media", "maior_cpu", "maior_ram",
    "tendencia_cpu", "tendencia_ram", "criticos", "atencao", "ok",
}


def medicao(cpu, ram, status="OK"):
    # No CSV, os valores chegam como texto; imitamos isso aqui.
    return {"cpu": str(cpu), "ram": str(ram), "status_geral": status}


def test_historico_vazio_tem_todas_as_chaves():
    resultado = analisar_historico([])

    assert set(resultado) == CHAVES
    assert resultado["quantidade"] == 0


def test_historico_medias_e_maximos():
    medicoes = [medicao(10, 20), medicao(30, 40), medicao(50, 60)]

    resultado = analisar_historico(medicoes)

    assert resultado["quantidade"] == 3
    assert resultado["cpu_media"] == pytest.approx(30)
    assert resultado["ram_media"] == pytest.approx(40)
    assert resultado["maior_cpu"] == 50
    assert resultado["maior_ram"] == 60


def test_historico_conta_status():
    medicoes = [
        medicao(10, 10, "CRÍTICO"),
        medicao(10, 10, "CRÍTICO"),
        medicao(10, 10, "ATENÇÃO"),
        medicao(10, 10, "OK"),
        medicao(10, 10, "OK"),
        medicao(10, 10, "OK"),
    ]

    resultado = analisar_historico(medicoes)

    assert resultado["criticos"] == 2
    assert resultado["atencao"] == 1
    assert resultado["ok"] == 3


def test_historico_ignora_medicoes_invalidas():
    medicoes = [
        medicao(10, 10),
        {"cpu": "abc", "ram": "20", "status_geral": "OK"},  # não numérico
        medicao(150, 50),                                    # fora de 0-100
        {"ram": "20", "status_geral": "OK"},                 # sem a chave cpu
        medicao(30, 30),
    ]

    resultado = analisar_historico(medicoes)

    assert resultado["cpu_media"] == pytest.approx(20)
    assert resultado["ram_media"] == pytest.approx(20)


def test_historico_todas_invalidas():
    medicoes = [{"cpu": "x", "ram": "y", "status_geral": "OK"}]

    resultado = analisar_historico(medicoes)

    assert set(resultado) == CHAVES
    assert resultado["quantidade"] == 0
    assert resultado["cpu_media"] == 0
    assert resultado["tendencia_cpu"] == "DADOS INSUFICIENTES"
    assert resultado["tendencia_ram"] == "DADOS INSUFICIENTES"


TENDENCIAS = [
    ([50, 50, 60, 60], "PIORANDO"),
    ([60, 60, 50, 50], "MELHORANDO"),
    ([50, 50, 51, 51], "ESTÁVEL"),
    ([50, 50, 52, 52], "ESTÁVEL"),  # diferença de exatamente 2 ainda é estável
    ([50, 50, 60], "DADOS INSUFICIENTES"),  # menos de 4 medições
]


@pytest.mark.parametrize("valores, esperado", TENDENCIAS)
def test_historico_tendencia_cpu(valores, esperado):
    medicoes = [medicao(v, 50) for v in valores]

    assert analisar_historico(medicoes)["tendencia_cpu"] == esperado


@pytest.mark.parametrize("valores, esperado", TENDENCIAS)
def test_historico_tendencia_ram(valores, esperado):
    medicoes = [medicao(50, v) for v in valores]

    assert analisar_historico(medicoes)["tendencia_ram"] == esperado