import csv
from datetime import datetime
from pathlib import Path

from historico import FORMATO_DATA, _conectar, _criar_tabela

ARQUIVO_CSV = Path("dados/historico.csv")


def migrar():
    if not ARQUIVO_CSV.exists():
        print("Arquivo dados/historico.csv não encontrado. Nada a migrar.")
        return

    inseridas = 0
    ignoradas = 0

    with _conectar() as conexao:
        _criar_tabela(conexao)

        with open(ARQUIVO_CSV, "r", newline="", encoding="utf-8") as arquivo:
            for linha in csv.DictReader(arquivo):
                data_hora = datetime.strptime(linha["data_hora"], FORMATO_DATA)

                ja_existe = conexao.execute(
                    "SELECT 1 FROM historico WHERE data_hora = %s AND computador = %s",
                    (data_hora, linha["computador"]),
                ).fetchone()

                if ja_existe:
                    ignoradas += 1
                    continue

                conexao.execute(
                    """
                    INSERT INTO historico
                        (data_hora, computador, cpu, ram, disco, internet, status_geral)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        data_hora,
                        linha["computador"],
                        linha["cpu"],
                        linha["ram"],
                        linha["disco"],
                        linha["internet"],
                        linha["status_geral"],
                    ),
                )
                inseridas += 1

    print(f"Migração concluída: {inseridas} inseridas, {ignoradas} já existiam.")


if __name__ == "__main__":
    migrar()