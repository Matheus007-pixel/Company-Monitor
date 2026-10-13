import pandas as pd
import streamlit as st
import monitor

from analise import analisar_computador, obter_status_geral, analisar_historico
from historico import ler_historico, registrar_medicao


st.set_page_config(
    page_title="Company Monitor",
    page_icon="🖥️",
    layout="wide"
)


def exibir_status(status, texto):
    if status == "OK":
        st.success(texto)
    elif status == "ATENÇÃO":
        st.warning(texto)
    elif status == "CRÍTICO":
        st.error(texto)
    else:
        st.info(texto)


st.title("🖥️ Company Monitor")
st.caption("Monitoramento e análise de desempenho do computador")

# Coleta os dados reais do computador
dados = monitor.coletar_informacoes()

analise = analisar_computador(
    dados["cpu"],
    dados["ram"],
    dados["disco"],
    dados["internet"]
)

status_geral = obter_status_geral(analise)

tab_resumo, tab_graficos, tab_processos, tab_historico = st.tabs([
    "Resumo",
    "Gráficos",
    "Processos",
    "Histórico"
])

# --- Aba Resumo ---
with tab_resumo:
    st.subheader("Desempenho em tempo real")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("CPU", f"{dados['cpu']}%")

    with col2:
        st.metric("RAM", f"{dados['ram']}%")

    with col3:
        st.metric("Disco", f"{dados['disco']}%")

    st.divider()

    st.subheader("Diagnóstico do computador")

    exibir_status(status_geral, f"**Status geral: {status_geral}**")

    col_cpu, col_ram, col_disco, col_internet = st.columns(4)

    for coluna, recurso in [
        (col_cpu, "cpu"),
        (col_ram, "ram"),
        (col_disco, "disco"),
        (col_internet, "internet")
    ]:
        with coluna:
            st.markdown(f"**{recurso.upper()}**")
            exibir_status(
                analise[recurso]["status"],
                analise[recurso]["status"]
            )
            st.caption(analise[recurso]["mensagem"])

# --- Aba Histórico ---
# Fica antes da aba Gráficos no código para que o botão registre a medição
# antes de o gráfico ler o CSV. Na tela, a ordem das abas continua a mesma.
with tab_historico:
    st.subheader("Histórico de desempenho")

    if st.button("Registrar medição no histórico"):
        registrar_medicao(dados, status_geral)
        st.success("Medição registrada.")

    medicoes = ler_historico()

    dados_grafico = []

    for medicao in medicoes:
        dados_grafico.append({
            "Data e hora": medicao["data_hora"],
            "CPU": float(medicao["cpu"]),
            "RAM": float(medicao["ram"])
        })

    if dados_grafico:
        st.caption("Últimas 10 medições, da mais recente para a mais antiga")

        for medicao in reversed(dados_grafico[-10:]):
            st.write(
                f"**{medicao['Data e hora']}** — "
                f"CPU: {medicao['CPU']:.1f}% | "
                f"RAM: {medicao['RAM']:.1f}%"
            )
    else:
        st.info("Ainda não existem medições no histórico.")

# --- Aba Gráficos ---
with tab_graficos:
    st.subheader("Evolução de CPU e RAM")

    if dados_grafico:
        df = pd.DataFrame(dados_grafico)
        df["Data e hora"] = pd.to_datetime(
            df["Data e hora"],
            format="%d/%m/%Y %H:%M:%S"
        )
        df = df.set_index("Data e hora")

        st.line_chart(df[["CPU", "RAM"]])

        st.divider()
        st.subheader("Indicadores históricos")

        resumo = analisar_historico(medicoes)

        h1, h2, h3, h4 = st.columns(4)
        h1.metric("Medições", resumo["quantidade"])
        h2.metric("CPU média", f"{resumo['cpu_media']:.1f}%")
        h3.metric("RAM média", f"{resumo['ram_media']:.1f}%")
        h4.metric("Críticas", resumo["criticos"])

        h5, h6, h7, h8 = st.columns(4)
        h5.metric("Maior CPU", f"{resumo['maior_cpu']:.1f}%")
        h6.metric("Maior RAM", f"{resumo['maior_ram']:.1f}%")
        h7.metric("Tendência CPU", resumo["tendencia_cpu"])
        h8.metric("Tendência RAM", resumo["tendencia_ram"])
    else:
        st.info("Ainda não existem medições no histórico.")

# --- Aba Processos ---
with tab_processos:
    st.subheader("Processos com maior consumo de RAM")

    processos = dados["processos"]

    if processos:
        for processo in processos:
            st.write(
                f"**{processo['nome']}** — "
                f"{processo['memoria']:.2f}% de RAM "
                f"({processo['memoria_mb']:.2f} MB)"
            )
    else:
        st.info("Nenhum processo disponível para exibição.")

    with st.expander("Dados brutos (depuração)"):
        st.json(dados)