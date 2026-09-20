def analisar_cpu(uso_cpu):
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
