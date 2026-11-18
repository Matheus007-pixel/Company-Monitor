import os
import secrets

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

from analise import analisar_computador, analisar_processos, obter_status_geral
from historico import ler_historico, registrar_medicao
from monitor import coletar_informacoes, obter_processos

load_dotenv()

app = FastAPI(title="Company Monitor API")

cabecalho_chave = APIKeyHeader(name="X-API-Key", auto_error=False)


class Medicao(BaseModel):
    computador: str = Field(min_length=1)
    cpu: float = Field(ge=0, le=100)
    ram: float = Field(ge=0, le=100)
    disco: float = Field(ge=0, le=100)
    internet: bool


def exigir_chave(chave: str | None = Security(cabecalho_chave)):
    esperada = os.environ.get("API_KEY")
    if not esperada:
        raise HTTPException(
            status_code=503,
            detail="Recebimento de medições desativado: API_KEY não configurada.",
        )

    if not chave or not secrets.compare_digest(chave.encode(), esperada.encode()):
        raise HTTPException(status_code=401, detail="Chave inválida ou ausente.")


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


@app.post("/medicoes", status_code=201, dependencies=[Depends(exigir_chave)])
def receber_medicao(medicao: Medicao):
    informacoes = medicao.model_dump()

    analise = analisar_computador(
        informacoes["cpu"],
        informacoes["ram"],
        informacoes["disco"],
        informacoes["internet"],
    )
    status_geral = obter_status_geral(analise)

    registrar_medicao(informacoes, status_geral)

    return {
        "status": "registrada",
        "computador": informacoes["computador"],
        "status_geral": status_geral,
    }