# Company Monitor

Sistema de monitoramento e análise de computadores desenvolvido em Python.

O projeto coleta métricas da máquina, analisa os recursos do sistema e identifica processos com maior consumo de memória.

## Tecnologias

* Python
* psutil
* socket
* pathlib
* datetime

## Funcionalidades

* Monitoramento de CPU, RAM e disco
* Verificação da conexão com a internet
* Identificação do sistema operacional
* Monitoramento do uptime
* Classificação dos recursos em `OK`, `ATENÇÃO` e `CRÍTICO`
* Definição de status geral da máquina
* Identificação dos processos com maior consumo de RAM
* Consumo de memória por processo em porcentagem e MB

## Estrutura

```text
Company-Monitor/
 main.py       # Execução principal
monitor.py    # Coleta dos dados
analise.py    # Análise dos dados
README.md     # Documentação principal
 docs/
    └── evolucao.md
```

## Exemplo de execução

```text
Uso da CPU: 9.3%
Uso da RAM: 91.5%
Uso do Disco: 19.4%

--- ANÁLISE DO COMPUTADOR ---
CPU: OK - Uso da CPU normal.
RAM: CRÍTICO - Uso da RAM muito alto.
Disco: OK - Espaço em disco normal.
Internet: OK - Internet funcionando normalmente.

STATUS GERAL: CRÍTICO
Computador: Menezes
Uptime: 134 horas, 37 minutos
Sistema Operacional: Windows

--- PROCESSOS COM MAIOR CONSUMO DE RAM ---
pycharm64.exe - 16.26% - 1289.03 MB
chrome.exe - 4.87% - 386.42 MB
Spotify.exe - 3.56% - 282.45 MB
```

## Roadmap

* [x] Monitoramento básico do sistema
* [x] Análise de CPU, RAM, disco e internet
* [x] Status geral da máquina
* [x] Monitoramento de processos
* [x] Consumo de RAM em % e MB
* [ ] Diagnóstico avançado dos processos
* [ ] Histórico de métricas
* [ ] Banco de dados
* [ ] API com FastAPI
* [ ] Dashboard web
* [ ] Docker
* [ ] Monitoramento de múltiplas máquinas
* [ ] Deploy em cloud

## Documentação

A evolução técnica e as decisões tomadas durante o desenvolvimento estão documentadas em [`docs/evolucao.md`](docs/evolucao.md).
