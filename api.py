from fastapi import FastAPI

from analise import analisar_computador, analisar_processos, obter_status_geral
from historico import ler_historico
from monitor import coletar_informacoes, obter_processos

app = FastAPI(title="Company Monitor API")

@app.get("/saude")
def saude():
    return {"status": "ok"}


@app.get("/historico")
def historico():
    return ler_historico()

@app.get("/status")
def status():
    informacoes = coletar_informacoes()

    analise = analisar_computador(
        informacoes["cpu"],
        informacoes["ram"],
        informacoes["disco"],
        informacoes["internet"],
    )

    return {
        "computador": informacoes["computador"],
        "sistema": informacoes["sistema"],
        "uptime": informacoes["uptime"],
        "cpu": informacoes["cpu"],
        "ram": informacoes["ram"],
        "disco": informacoes["disco"],
        "internet": informacoes["internet"],
        "analise": analise,
        "status_geral": obter_status_geral(analise),
    }

@app.get("/processos")
def processos():
    return analisar_processos(obter_processos())