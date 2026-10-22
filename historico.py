import os
from datetime import datetime

import psycopg
from dotenv import load_dotenv

load_dotenv()
COLUNAS = [
    "data_hora",
    "computador",
    "cpu",
    "ram",
    "disco",
    "internet",
    "status_geral",
]

FORMATO_DATA = "%d/%m/%Y %H:%M:%S"


def _conectar():
    senha = os.environ.get("DB_PASSWORD")
    if not senha:
        raise RuntimeError("Variável de ambiente DB_PASSWORD não definida.")

    return psycopg.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "company_monitor"),
        user=os.environ.get("DB_USER", "monitor_app"),
        password=senha,
    )


def _criar_tabela(conexao):
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            data_hora TIMESTAMP NOT NULL,
            computador TEXT NOT NULL,
            cpu TEXT NOT NULL,
            ram TEXT NOT NULL,
            disco TEXT NOT NULL,
            internet TEXT NOT NULL,
            status_geral TEXT NOT NULL
        )
    """)


def registrar_medicao(informacoes, status_geral):
    with _conectar() as conexao:
        _criar_tabela(conexao)
        conexao.execute(
            """
            INSERT INTO historico
                (data_hora, computador, cpu, ram, disco, internet, status_geral)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                datetime.now(),
                str(informacoes["computador"]),
                str(informacoes["cpu"]),
                str(informacoes["ram"]),
                str(informacoes["disco"]),
                str(informacoes["internet"]),
                status_geral,
            ),
        )


def ler_historico():
    with _conectar() as conexao:
        _criar_tabela(conexao)
        linhas = conexao.execute(
            """
            SELECT data_hora, computador, cpu, ram, disco, internet, status_geral
            FROM historico
            ORDER BY data_hora, id
            """
        ).fetchall()

    medicoes = []
    for linha in linhas:
        medicao = dict(zip(COLUNAS, linha))
        medicao["data_hora"] = medicao["data_hora"].strftime(FORMATO_DATA)
        medicoes.append(medicao)

    return medicoes