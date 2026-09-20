import psutil
import socket
import platform
import datetime

def obter_cpu():
    return psutil.cpu_percent(interval=1)

def obter_ram():
    ram = psutil.virtual_memory()
    return ram.percent

def obter_disco():
    disco = psutil.disk_usage("C:\\")
    return disco.percent

def verificar_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def obter_nome_computador():
    return platform.node()

def obter_sistema_operacional():
    return platform.system()

def coletar_informacoes():
    return {
        "cpu": obter_cpu(),
        "ram": obter_ram(),
        "disco": obter_disco(),
        "internet": verificar_internet(),
        "computador": obter_nome_computador(),
        "uptime": obter_uptime(),
        "sistema": obter_sistema_operacional(),
        "processos": obter_processos()
    }

    return informacoes

def obter_uptime():
    inicio = psutil.boot_time()
    agora = datetime.datetime.now().timestamp()

    uptime = agora - inicio

    horas = int(uptime // 3600)
    minutos = int((uptime % 3600) // 60)

    return f"{horas} horas, {minutos} minutos"

def obter_processos():
    processos = []

    for processo in psutil.process_iter(["name", "memory_percent", "memory_info"]):
        try:
            memoria_percentual = processo.info["memory_percent"]
            memoria_mb = processo.info["memory_info"].rss / (1024 * 1024)

            processos.append({
                "nome": processo.info["name"],
                "memoria": memoria_percentual,
                "memoria_mb": memoria_mb
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processos.sort(key=lambda processo: processo["memoria"], reverse=True)

    return processos[:10]

