from fastapi import FastAPI

from historico import ler_historico

app = FastAPI(title="Company Monitor API")


@app.get("/saude")
def saude():
    return {"status": "ok"}


@app.get("/historico")
def historico():
    return ler_historico()