import csv
from pathlib import Path
from datetime import datetime

ARQUIVO_HISTORICO = Path("dados/historico.csv")

def registrar_medicao (informacoes, status_geral):
    arquivo_existe = ARQUIVO_HISTORICO.exists()

    with open(ARQUIVO_HISTORICO, "a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)

        if not arquivo_existe:
            escritor.writerow([
                "data_hora",
                "computador",
                "cpu",
                "ram",
                "disco",
                "internet",
                "status_geral"
            ])

        escritor.writerow([
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            informacoes["computador"],
            informacoes["cpu"],
            informacoes["ram"],
            informacoes["disco"],
            informacoes["internet"],
            status_geral
        ])


