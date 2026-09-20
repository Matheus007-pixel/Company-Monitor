# Evolução do Company Monitor

Este documento registra a evolução técnica do Company Monitor, incluindo as funcionalidades implementadas, decisões de desenvolvimento e próximos passos.

---

## Fase 1 — Monitoramento básico

O projeto começou como uma aplicação local para coleta de informações do computador utilizando Python e `psutil`.

Foram implementados os primeiros indicadores:

* Uso da CPU
* Uso da memória RAM
* Uso do disco
* Conectividade com a internet
* Nome do computador
* Sistema operacional
* Uptime

A coleta foi centralizada no módulo `monitor.py`.

---

## Fase 2 — Separação de responsabilidades

O código foi dividido em módulos para evitar que toda a lógica ficasse concentrada no arquivo principal.

### `monitor.py`

Responsável pela coleta das informações do sistema.

### `analise.py`

Responsável pela interpretação dos dados coletados.

### `main.py`

Responsável por coordenar a execução e apresentar os resultados.

Essa separação permite que cada módulo tenha uma responsabilidade específica e facilita a evolução futura do projeto.

---

## Fase 3 — Análise dos recursos

Foi implementado um sistema de classificação dos recursos monitorados.

### CPU

* Abaixo de 70% → `OK`
* De 70% até 89% → `ATENÇÃO`
* A partir de 90% → `CRÍTICO`

### RAM

* Abaixo de 70% → `OK`
* De 70% até 89% → `ATENÇÃO`
* A partir de 90% → `CRÍTICO`

### Disco

* Abaixo de 75% → `OK`
* De 75% até 89% → `ATENÇÃO`
* A partir de 90% → `CRÍTICO`

### Internet

* Conectada → `OK`
* Sem conexão → `CRÍTICO`

Também foi criado um status geral para a máquina, seguindo a prioridade:

```text
CRÍTICO
   ↓
ATENÇÃO
   ↓
OK
```

Se qualquer recurso estiver em estado `CRÍTICO`, o status geral será `CRÍTICO`.

Caso não exista nenhum estado crítico, mas exista algum estado de atenção, o resultado será `ATENÇÃO`.

---

## Fase 4 — Monitoramento de processos

Como a utilização de RAM da máquina apresentava valores elevados durante os testes, foi implementado o monitoramento dos processos em execução.

O sistema passou a:

* Identificar processos em execução
* Obter o consumo percentual de memória
* Obter o consumo de memória em MB
* Ordenar os processos pelo consumo
* Selecionar os 10 maiores consumidores

Durante os testes, o sistema identificou o `pycharm64.exe` como o processo individual com maior consumo de memória.

Exemplo:

```text
pycharm64.exe - 16.26% - 1289.03 MB
chrome.exe - 4.87% - 386.42 MB
Spotify.exe - 3.56% - 282.45 MB
```

Essa funcionalidade permitiu evoluir o projeto de um simples monitor de recursos para uma ferramenta capaz de auxiliar na identificação das possíveis fontes de consumo elevado.

---

## Fase atual

O projeto atualmente possui:

* Coleta de métricas do sistema
* Análise dos principais recursos
* Status geral da máquina
* Monitoramento dos processos
* Identificação dos maiores consumidores de RAM
* Consumo de memória em porcentagem e MB

A próxima etapa é ampliar a análise dos processos e transformar os dados coletados em diagnósticos mais detalhados.

---

## Próximas etapas

A evolução planejada do projeto inclui:

1. Diagnóstico avançado dos processos
2. Monitoramento de processos com alto consumo de CPU
3. Armazenamento histórico das métricas
4. Persistência em banco de dados
5. Criação de uma API com FastAPI
6. Desenvolvimento de dashboard web
7. Containerização com Docker
8. Suporte ao monitoramento de múltiplas máquinas
9. Infraestrutura e deploy em cloud

O objetivo final é transformar o protótipo local em uma solução de monitoramento capaz de acompanhar múltiplos computadores e disponibilizar os dados por meio de uma aplicação web.
