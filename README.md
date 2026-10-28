# Company Monitor

Aplicação de monitoramento e análise de desempenho de computadores, desenvolvida em Python para Windows.

O projeto coleta métricas da máquina, classifica o estado dos recursos, identifica os processos que mais consomem memória, guarda um histórico das medições em um banco PostgreSQL e apresenta tudo em um dashboard web feito com Streamlit. Os dados também ficam disponíveis por uma API REST com FastAPI. Também pode ser executado no terminal.

![Dashboard do Company Monitor](docs/dashboard.png)

## Tecnologias

* Python
* Streamlit (dashboard web)
* FastAPI (API REST)
* PostgreSQL com psycopg (histórico das medições)
* python-dotenv (configuração por variáveis de ambiente)
* Pandas (gráficos e filtros do histórico)
* psutil (coleta de dados do sistema)
* pytest e httpx (testes automatizados, incluindo a API)
* Biblioteca padrão: `socket`, `pathlib`, `datetime`, `csv`

## Funcionalidades

* Monitoramento de CPU, RAM e disco
* Verificação da conexão com a internet
* Identificação do sistema operacional, nome do computador e uptime
* Classificação dos recursos em `OK`, `ATENÇÃO`, `CRÍTICO` e `INDISPONÍVEL`
* Definição do status geral da máquina
* Identificação dos processos com maior consumo de RAM, em porcentagem e MB, somando as instâncias do mesmo programa
* Histórico de medições salvo em PostgreSQL
* Indicadores históricos: médias, valores máximos, tendência de CPU e RAM e contagem de medições por estado
* Dashboard web com diagnósticos coloridos por gravidade
* Dashboard organizado em quatro abas: Resumo, Gráficos, Processos e Histórico
* Atualização automática a cada 5 segundos, que pode ser pausada na barra lateral
* Gráficos históricos de CPU, RAM e disco, com filtro de período e seleção de métricas
* Registro manual de medições pelo dashboard
* Tabelas com barras de progresso nas abas Processos e Histórico
* Faixa de status colorida com o diagnóstico dos processos
* Download do histórico completo em CSV, com abertura direta no Excel
* API REST com endpoints de saúde, status atual, processos e histórico, com documentação automática em `/docs`

## Requisitos

* Python 3.14
* PostgreSQL 18
* Windows (a coleta de disco usa o drive `C:\`)

## Como executar

1. Clone o repositório e entre na pasta do projeto:
```bash
git clone https://github.com/Matheus007-pixel/Company-Monitor.git
cd Company-Monitor
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados (veja a seção abaixo).

5. Execute o dashboard:
```bash
python -m streamlit run dashboard.py
```

Ou execute a versão de terminal:

```bash
python main.py
```

Ou suba a API:

```bash
fastapi dev api.py
```

Com a API no ar, a documentação interativa fica em `http://127.0.0.1:8000/docs`.

## Configuração do banco de dados

O histórico fica em um banco PostgreSQL. A tabela `historico` é criada automaticamente na primeira execução.

1. Crie dois bancos no PostgreSQL: `company_monitor` (dados reais) e `company_monitor_test` (usado só pelos testes).

2. Copie o arquivo de exemplo e preencha a senha:
```bash
copy .env.example .env
```

3. Edite o `.env`. O arquivo está no `.gitignore` e nunca deve ser enviado ao GitHub.

| Variável | Obrigatória | Padrão |
| --- | --- | --- |
| `DB_PASSWORD` | Sim | (sem padrão) |
| `DB_HOST` | Não | `localhost` |
| `DB_PORT` | Não | `5432` |
| `DB_NAME` | Não | `company_monitor` |
| `DB_USER` | Não | `monitor_app` |

4. Se já existir um histórico antigo em CSV (`dados/historico.csv`), importe-o para o banco. O script não duplica medições se for executado mais de uma vez:
```bash
python migrar_csv.py
```

## API

| Método | Endpoint | Descrição |
| --- | --- | --- |
| GET | `/saude` | Confirma que a API está no ar |
| GET | `/status` | Medição atual de CPU, RAM, disco e internet, com análise e status geral |
| GET | `/processos` | Processos que mais consomem memória, com diagnóstico |
| GET | `/historico` | Histórico de medições salvo no banco |

<!-- Quando a captura estiver salva em docs/api-docs.png, remova os marcadores de comentário desta linha:
![Documentação da API em /docs](docs/api-docs.png)
-->

## Testes

O projeto tem testes automatizados com pytest. Eles cobrem os limites de classificação, o status geral, os processos, o histórico, o acesso ao banco e os endpoints da API.

```bash
python -m pytest -v
```

Os testes de banco usam o `company_monitor_test`, com uma trava que confere o nome do banco antes de apagar dados, então o banco real não é afetado. Os testes da API usam dados fixos no lugar da coleta real do sistema e do banco.

## Estrutura

```text
Company-Monitor/
├── dados/
│   └── historico.csv   # Histórico antigo em CSV (usado só na migração, se existir)
├── docs/
│   ├── dashboard.png   # Captura de tela do dashboard
│   └── evolucao.md     # Evolução técnica e decisões
├── tests/
│   ├── test_analise.py            # Testes das funções de classificação
│   ├── test_analisar_historico.py # Testes dos indicadores históricos
│   ├── test_historico.py          # Testes da gravação e leitura no PostgreSQL
│   └── test_api.py                # Testes dos endpoints da API
├── analise.py          # Classificação e análise dos dados
├── api.py              # API REST com FastAPI
├── dashboard.py        # Interface web com Streamlit
├── historico.py        # Leitura e gravação do histórico no PostgreSQL
├── main.py             # Execução no terminal
├── migrar_csv.py       # Importa o histórico antigo em CSV para o banco
├── monitor.py          # Coleta dos dados do sistema
├── pytest.ini          # Configuração do pytest
├── requirements.txt    # Dependências do projeto
├── .env.example        # Modelo das variáveis de ambiente (sem senha)
└── README.md           # Documentação principal
```

## Exemplo de execução no terminal

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
* [x] Histórico de métricas
* [x] Dashboard web
* [x] Indicadores históricos e tendências
* [x] Gráficos históricos de CPU e RAM
* [x] Testes automatizados com pytest
* [x] Agrupamento de processos por nome
* [x] Banco de dados PostgreSQL
* [x] API com FastAPI
* [x] Testes da API
* [ ] Refinar os tipos das colunas do banco (numéricos e booleano)
* [ ] Diagnóstico avançado dos processos
* [ ] Docker (docker-compose para o banco)
* [ ] Monitoramento de múltiplas máquinas
* [ ] Deploy em cloud

## Documentação

A evolução técnica e as decisões tomadas durante o desenvolvimento estão documentadas em [`docs/evolucao.md`](docs/evolucao.md).