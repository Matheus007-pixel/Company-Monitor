import streamlit as st
import monitor

from analise import analisar_computador, obter_status_geral
from historico import ler_historico


st.set_page_config(
    page_title="Company Monitor",
    page_icon="🖥️",
    layout="wide"
)

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

st.metric("Status geral", status_geral)

col_cpu, col_ram, col_disco, col_internet = st.columns(4)

for coluna, recurso in [
    (col_cpu, "cpu"),
    (col_ram, "ram"),
    (col_disco, "disco"),
    (col_internet, "internet")
]:
    with coluna:
        st.markdown(f"**{recurso.upper()}**")
        st.write(f"Status: {analise[recurso]['status']}")
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





st.subheader("Dados coletados")
st.json(dados)