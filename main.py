from monitor import coletar_informacoes
from analise import analisar_computador, analisar_processos, obter_status_geral,analisar_historico
from historico import registrar_medicao, ler_historico


informacoes = coletar_informacoes()

analise = analisar_computador(
    informacoes["cpu"],
    informacoes["ram"],
    informacoes["disco"],
    informacoes["internet"]
)

status_geral = obter_status_geral(analise)

registrar_medicao(informacoes, status_geral)

medicoes = ler_historico()

analise_historico = analisar_historico(medicoes)


analise_processos = analisar_processos(informacoes["processos"])

print(f"Uso da CPU: {informacoes['cpu']}%")
print(f"Uso da RAM: {informacoes['ram']}%")
print(f"Uso do Disco: {informacoes['disco']}%")

print("\n--- ANÁLISE DO COMPUTADOR ---")
print(f"CPU: {analise['cpu']['status']} - {analise['cpu']['mensagem']}")
print(f"RAM: {analise['ram']['status']} - {analise['ram']['mensagem']}")
print(f"Disco: {analise['disco']['status']} - {analise['disco']['mensagem']}")
print(f"Internet: {analise['internet']['status']} - {analise['internet']['mensagem']}")

print(f"\nSTATUS GERAL: {status_geral}")

print(f"Computador: {informacoes['computador']}")
print(f"Uptime: {informacoes['uptime']}")
print(f"Sistema Operacional: {informacoes['sistema']}")

print("\n--- PROCESSOS COM MAIOR CONSUMO DE RAM ---")

print(
    f"\nDiagnóstico dos processos: "
    f"{analise_processos['status']} - "
    f"{analise_processos['mensagem']}"
)

for processo in informacoes["processos"]:
    print(
        f"{processo['nome']} - "
        f"{processo['memoria']:.2f}% - "
        f"{processo['memoria_mb']:.2f} MB"
    )

print("\n--- ANÁLISE DO HISTÓRICO ---")

print(f"Quantidade de medições: {analise_historico['quantidade']}")
print(f"CPU média: {analise_historico['cpu_media']:.2f}%")
print(f"RAM média: {analise_historico['ram_media']:.2f}%")
print(f"Maior CPU: {analise_historico['maior_cpu']:.2f}%")
print(f"Maior RAM: {analise_historico['maior_ram']:.2f}%")
print(f"Medições críticas: {analise_historico['criticos']}")
print(f"Medições em atenção: {analise_historico['atencao']}")
print(f"Medições normais: {analise_historico['ok']}")