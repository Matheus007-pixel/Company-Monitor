def analisar_cpu(uso_cpu):
    if uso_cpu is None:
        return {
            "status": "INDISPONÍVEL",
            "mensagem": "Não foi possível obter o uso da CPU."
        }
    if uso_cpu >= 90:
        return {
            "status": "CRÍTICO",
            "mensagem": "Uso da CPU muito alto."
        }
    elif uso_cpu >= 70:
        return {
            "status": "ATENÇÃO",
            "mensagem": "Uso da CPU elevado."
        }
    else:
        return {
            "status": "OK",
            "mensagem": "Uso da CPU normal."
        }

def analisar_ram(uso_ram):
    if uso_ram is None:
        return {
            "status": "INDISPONÍVEL",
            "mensagem": "Não foi possível obter o uso da RAM."
        }

    if uso_ram >= 90:
        return {
            "status": "CRÍTICO",
            "mensagem": "Uso da RAM muito alto."
        }
    elif uso_ram >= 70:
        return {
            "status": "ATENÇÃO",
            "mensagem": "Uso da RAM elevado."
        }
    else:
        return {
            "status": "OK",
            "mensagem": "Uso da RAM normal."
        }

def analisar_disco(uso_disco):
    if uso_disco is None:
        return {
            "status": "INDISPONÍVEL",
            "mensagem": "Não foi possível obter o uso do disco."
        }

    if uso_disco >= 90:
        return {
            "status": "CRÍTICO",
            "mensagem": "Espaço em disco muito baixo."
        }
    elif uso_disco >= 75:
        return {
            "status": "ATENÇÃO",
            "mensagem": "Espaço em disco começando a ficar baixo."
        }
    else:
        return {
            "status": "OK",
            "mensagem": "Espaço em disco normal."
        }

def analisar_internet(status_internet):
    if status_internet:
        return {
            "status": "OK",
            "mensagem": "Internet funcionando normalmente."
        }
    else:
        return {
            "status": "CRÍTICO",
            "mensagem": "Sem conexão com a internet."
        }
def analisar_computador(cpu, ram, disco, internet):
    return {
        "cpu": analisar_cpu(cpu),
        "ram": analisar_ram(ram),
        "disco": analisar_disco(disco),
        "internet": analisar_internet(internet)
    }

def obter_status_geral(analise):
    status = [
        analise["cpu"]["status"],
        analise["ram"]["status"],
        analise["disco"]["status"],
        analise["internet"]["status"]
    ]

    if "CRÍTICO" in status:
        return "CRÍTICO"
    elif "ATENÇÃO" in status:
        return "ATENÇÃO"
    else:
        return "OK"

def analisar_processos(processos):
    if not processos:
        return {
            "status": "OK",
            "mensagem": "Nenhum processo encontrado.",
            "processos": []
        }

    maior_processo = processos[0]

    if maior_processo["memoria"] >= 20:
        status = "CRÍTICO"
        mensagem = (
            f"O processo {maior_processo['nome']} "
            f"está consumindo muita memória."
        )
    elif maior_processo["memoria"] >= 10:
        status = "ATENÇÃO"
        mensagem = (
            f"O processo {maior_processo['nome']} "
            f"está entre os maiores consumidores de memória."
        )
    else:
        status = "OK"
        mensagem = "Nenhum processo apresenta consumo elevado de memória."

    return {
        "status": status,
        "mensagem": mensagem,
        "processos": processos
    }

def analisar_historico(medicoes):
    if not medicoes:
        return {
            "quantidade": 0,
            "cpu_media":0,
            "ram_media": 0,
            "maior_cpu": 0,
            "maior_ram": 0,
            "criticos": 0,
            "atencao": 0,
            "ok": 0

        }
    cpus = []
    rams = []

    for medicao in medicoes:
        try:
            cpu = float(medicao["cpu"])
            ram = float(medicao["ram"])
        except (ValueError, TypeError, KeyError):
            continue

        if not (0 <= cpu <= 100 and 0 <= ram <= 100):
            continue

        cpus.append(cpu)
        rams.append(ram)

    if len(rams) >= 4:
        metade = len(rams) // 2

        ram_media_antiga = sum(rams[:metade]) / len(rams[:metade])
        ram_media_recente = sum(rams[metade:]) / len(rams[metade:])

        if ram_media_recente > ram_media_antiga + 2:
            tendencia_ram = "PIORANDO"
        elif ram_media_recente < ram_media_antiga - 2:
            tendencia_ram = "MELHORANDO"
        else:
            tendencia_ram = "ESTÁVEL"
    else:
        tendencia_ram = "DADOS INSUFICIENTES"

    if len(cpus) >= 4:
        metade = len(cpus) // 2

        cpu_media_antiga = sum(cpus[:metade]) / len(cpus[:metade])
        cpu_media_recente = sum(cpus[metade:]) / len(cpus[metade:])

        if cpu_media_recente > cpu_media_antiga + 2:
            tendencia_cpu = "PIORANDO"
        elif cpu_media_recente < cpu_media_antiga - 2:
            tendencia_cpu = "MELHORANDO"
        else:
            tendencia_cpu = "ESTÁVEL"
    else:
        tendencia_cpu = "DADOS INSUFICIENTES"

    if not cpus or not rams:
        return {
            "quantidade": 0,
            "cpu_media": 0,
            "ram_media": 0,
            "maior_cpu": 0,
            "maior_ram": 0,
            "tendencia_cpu": "DADOS INSUFICIENTES",
            "tendencia_ram": "DADOS INSUFICIENTES",
            "criticos": 0,
            "atencao": 0,
            "ok": 0
        }

    criticos = sum(
        1 for medicao in medicoes
        if medicao["status_geral"] == "CRÍTICO"
    )

    atencao = sum(
        1 for medicao in medicoes
        if medicao["status_geral"] == "ATENÇÃO"
    )

    ok = sum(
        1 for medicao in medicoes
        if medicao["status_geral"] == "OK"
    )

    return {
        "quantidade": len(medicoes),
        "cpu_media": sum(cpus) / len(cpus),
        "ram_media": sum(rams) / len(rams),
        "tendencia_ram": tendencia_ram,
        "tendencia_cpu": tendencia_cpu,
        "maior_cpu": max(cpus),
        "maior_ram": max(rams),
        "criticos": criticos,
        "atencao": atencao,
        "ok": ok
    }

