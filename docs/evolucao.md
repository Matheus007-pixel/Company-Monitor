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

### Agrupamento por nome

Programas como o Chrome abrem vários processos com o mesmo nome, e listá-los separadamente escondia o consumo real. Por isso, os processos passaram a ser agrupados por nome, somando a porcentagem, os MB e contando as instâncias. A lista final mostra os 10 maiores grupos.

---

## Fase 5 — Histórico, indicadores e dashboard

Foi adicionado o registro de medições ao longo do tempo, inicialmente em um arquivo CSV.

Com o histórico, a análise ganhou indicadores:

* Médias de CPU e RAM
* Valores máximos
* Tendência de CPU e RAM (`PIORANDO`, `ESTÁVEL`, `MELHORANDO`), comparando a média da primeira metade das medições com a da segunda metade
* Contagem de medições por estado

A função de análise do histórico ignora medições corrompidas ou com valores fora de 0 a 100, para que um registro ruim não derrube os indicadores.

Em seguida foi criado o dashboard web com Streamlit, organizado em quatro abas: Resumo, Gráficos, Processos e Histórico. Ele atualiza automaticamente a cada 5 segundos, tem gráficos com filtro de período e permite registrar medições manualmente e baixar o histórico em CSV.

---

## Fase 6 — Testes automatizados

Foram criados testes com pytest para o módulo de análise, cobrindo os limites de classificação, o status geral, a análise dos processos, o agrupamento e os indicadores do histórico.

Os testes de limite são importantes porque as regras de classificação usam comparações como `>= 90`, e é nesses valores exatos que os erros costumam aparecer.

---

## Fase 7 — Migração do histórico para PostgreSQL

O histórico em CSV foi substituído por um banco PostgreSQL, acessado com `psycopg`.

Decisões tomadas:

* **Mesma interface.** `registrar_medicao` e `ler_historico` mantiveram a assinatura e o formato de retorno (lista de dicionários com todos os valores como texto). Assim, o dashboard e a análise continuaram funcionando sem alterações.
* **Colunas de texto por enquanto.** Com exceção de `data_hora` (`TIMESTAMP`), as colunas foram criadas como `TEXT`, para preservar o formato que o restante do código já esperava. Refinar os tipos (numéricos e booleano) ficou como etapa futura.
* **Tabela criada automaticamente.** O módulo cria a tabela `historico` se ela não existir, o que simplifica a primeira execução.
* **Configuração por ambiente.** A conexão usa variáveis de ambiente carregadas de um arquivo `.env`, que fica fora do Git. A senha é obrigatória e não tem valor padrão. Existe um `.env.example` sem senha como modelo.
* **Banco separado para testes.** Os testes rodam no `company_monitor_test`, com uma trava que confere o nome do banco antes de apagar dados. Isso evita que um teste limpe os dados reais por engano.
* **Migração dos dados antigos.** O script `migrar_csv.py` importou as medições do CSV e não duplica registros se for executado novamente.

---

## Fase 8 — API com FastAPI

Os dados passaram a ser expostos por uma API REST, com documentação automática em `/docs`.

Endpoints:

* `GET /saude` — confirma que a API está no ar
* `GET /status` — medição atual, com análise por recurso e status geral
* `GET /processos` — maiores consumidores de memória, com diagnóstico
* `GET /historico` — histórico salvo no banco

Decisões tomadas:

* **Reaproveitar a lógica existente.** Os endpoints apenas ligam as funções de `monitor.py`, `analise.py` e `historico.py`, sem duplicar regras de negócio na API.
* **Funções síncronas (`def`).** `psutil`, `socket` e `psycopg` são bloqueantes. Com `def`, o FastAPI executa as funções em uma thread separada e não trava o servidor.
* **Testes sem depender do computador.** Os testes usam o `TestClient` do FastAPI e `monkeypatch` para trocar a coleta do sistema e a leitura do banco por dados fixos. Assim os testes verificam a lógica da API de forma previsível, sem acessar o PC real nem o banco.

Neste ponto o projeto tem 62 testes passando.

---

## Fase atual

O projeto atualmente possui:

* Coleta de métricas do sistema
* Análise dos principais recursos e status geral da máquina
* Monitoramento e agrupamento dos processos por consumo de RAM
* Histórico em PostgreSQL, com indicadores e tendências
* Dashboard web com quatro abas
* API REST com quatro endpoints
* 62 testes automatizados

---

## Próximas etapas

1. Refinar o visual do dashboard (tema escuro e identidade própria)
2. Refinar os tipos das colunas do banco (numéricos e booleano)
3. docker-compose para subir o banco
4. Diagnóstico avançado dos processos
5. Monitoramento de processos com alto consumo de CPU
6. Suporte ao monitoramento de múltiplas máquinas
7. Deploy em cloud

O objetivo final é transformar o protótipo local em uma solução de monitoramento capaz de acompanhar múltiplos computadores e disponibilizar os dados por meio de uma aplicação web.