import streamlit as st
import monitor

from analise import analisar_computador, obter_status_geral, analisar_historico
from historico import ler_historico



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
st.caption("Monitoramento e análise de desempemho do computador")

st.subheader("Desempenho em tempo real")

# Coleta os dados reais do computador

dados = monitor.coletar_informacoes()


analise = analisar_computador(
    dados["cpu"],
    dados["ram"],
    dados["disco"],
    dados["internet"]
)

status_geral = obter_status_geral(analise)


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
        exibir_status(analise[recurso]["status"], analise[recurso]["status"])
        st.caption(analise[recurso]["mensagem"])




st.divider()

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


st.divider()

st.subheader("Histórico de desempenho")

medicoes = ler_historico()

if medicoes:
    dados_grafico = []

    for medicao in medicoes:
        dados_grafico.append({
            "Data e hora": medicao["data_hora"],
            "CPU": float(medicao["cpu"]),
            "RAM": float(medicao["ram"])
        })

    st.write("Histórico de CPU e RAM")

    for medicao in dados_grafico:
        st.write(
            f"**{medicao['Data e hora']}** — "
            f"CPU: {medicao['CPU']:.1f}% | "
            f"RAM: {medicao['RAM']:.1f}%"
        )
else:
    st.info("Ainda não existem medições no histórico.")

st.divider()
st.subheader("Indicadores históricos")

resumo = analisar_historico(ler_historico())

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


with st.expander("Dados brutos (depuração)"):
    st.json(dados)