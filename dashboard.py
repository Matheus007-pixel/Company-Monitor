from datetime import datetime

import pandas as pd
import streamlit as st
import monitor

from analise import (
    analisar_computador,
    obter_status_geral,
    analisar_historico,
    analisar_processos,

)
from historico import ler_historico, registrar_medicao


INTERVALO_ATUALIZACAO = 5  # segundos

st.set_page_config(
    page_title="Sentinela",
    page_icon=":material/shield:",
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


@st.cache_data(ttl=4)
def coletar_dados():
    # O cache de 4 segundos evita coletar duas vezes quando mais de um
    # trecho da página pede os dados quase ao mesmo tempo.
    return monitor.coletar_informacoes()


def obter_diagnostico():
    dados = coletar_dados()

    analise = analisar_computador(
        dados["cpu"],
        dados["ram"],
        dados["disco"],
        dados["internet"]
    )

    status_geral = obter_status_geral(analise)

    return dados, analise, status_geral


def painel_resumo():
    dados, analise, _ = obter_diagnostico()

    st.subheader("Visão geral")

    def percentual(valor):
        return f"{valor}%" if valor is not None else "—"

    col_cpu, col_ram, col_disco, col_internet = st.columns(4)

    for coluna, titulo, valor, recurso in [
        (col_cpu, "CPU", percentual(dados["cpu"]), "cpu"),
        (col_ram, "RAM", percentual(dados["ram"]), "ram"),
        (col_disco, "DISCO", percentual(dados["disco"]), "disco"),
        (
            col_internet,
            "INTERNET",
            "Online" if dados["internet"] else "Offline",
            "internet",
        ),
    ]:
        with coluna:
            cartao(
                titulo,
                valor,
                analise[recurso]["status"],
                analise[recurso]["mensagem"],
            )


def painel_processos():
    dados, _, _ = obter_diagnostico()

    st.subheader("Processos com maior consumo de RAM")

    processos = dados["processos"]

    if processos:
        resultado = analisar_processos(processos)
        exibir_status(resultado["status"], resultado["mensagem"])

        df = pd.DataFrame(processos)[
            ["nome", "quantidade", "memoria", "memoria_mb"]
        ]
        df.columns = ["Processo", "Instâncias", "RAM (%)", "RAM (MB)"]

        st.caption(
            "Processos com o mesmo nome foram somados. "
            "A lista considera os que mais consomem RAM."
        )

        st.dataframe(
            df,
            hide_index=True,
            width="stretch",
            column_config={
                "Instâncias": st.column_config.NumberColumn(
                    "Instâncias", format="%d"
                ),
                "RAM (%)": st.column_config.ProgressColumn(
                    "RAM (%)",
                    format="%.2f%%",
                    min_value=0,
                    max_value=float(df["RAM (%)"].max()),
                ),
                "RAM (MB)": st.column_config.NumberColumn(
                    "RAM (MB)",
                    format="%.1f"
                ),
            },
        )
    else:
        st.info("Nenhum processo disponível para exibição.")

    with st.expander("Dados brutos (depuração)"):
        st.json(dados)


CORES_STATUS = {
    "OK": "#00D4AA",
    "ATENÇÃO": "#F5B942",
    "CRÍTICO": "#FF5C5C",
    "INDISPONÍVEL": "#8A94A6",
}


def cabecalho():
    dados, _, status_geral = obter_diagnostico()
    cor = CORES_STATUS.get(status_geral, CORES_STATUS["INDISPONÍVEL"])
    hora = datetime.now().strftime("%H:%M:%S")

    html = (
        '<div style="display:flex;justify-content:space-between;'
        'align-items:center;padding-bottom:14px;margin-bottom:8px;'
        'border-bottom:1px solid #1E2A44;">'
        '<div>'
        '<div style="font-size:1.7rem;font-weight:700;'
        'letter-spacing:0.22em;">SENTINELA</div>'
        '<div style="font-size:0.85rem;color:#8A94A6;margin-top:2px;">'
        f'Monitoramento de desempenho &middot; {dados["computador"]}'
        '</div>'
        '</div>'
        '<div style="text-align:right;">'
        f'<div style="display:inline-block;padding:4px 14px;'
        f'border-radius:999px;border:1px solid {cor};'
        f'background:{cor}22;color:{cor};font-weight:600;'
        f'font-size:0.85rem;letter-spacing:0.08em;">'
        f'&#9679; {status_geral}</div>'
        '<div style="font-size:0.75rem;color:#8A94A6;margin-top:6px;">'
        f'Atualizado às {hora}</div>'
        '</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def cartao(titulo, valor, status, mensagem):
    cor = CORES_STATUS.get(status, CORES_STATUS["INDISPONÍVEL"])

    html = (
        '<div style="background:#111A2E;border:1px solid #1E2A44;'
        f'border-top:3px solid {cor};border-radius:10px;padding:16px 18px;">'
        '<div style="font-size:0.75rem;color:#8A94A6;'
        f'letter-spacing:0.12em;">{titulo}</div>'
        '<div style="font-size:2rem;font-weight:700;margin:4px 0 8px;">'
        f'{valor}</div>'
        '<div style="display:inline-block;padding:2px 10px;'
        f'border-radius:999px;border:1px solid {cor};'
        f'background:{cor}22;color:{cor};font-size:0.75rem;'
        f'font-weight:600;letter-spacing:0.08em;">{status}</div>'
        '<div style="font-size:0.8rem;color:#8A94A6;margin-top:8px;">'
        f'{mensagem}</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


atualizar = st.sidebar.toggle("Atualização automática", value=True)
st.sidebar.caption(f"Atualiza a cada {INTERVALO_ATUALIZACAO} segundos")

intervalo = INTERVALO_ATUALIZACAO if atualizar else None

st.fragment(cabecalho, run_every=intervalo)()

tab_resumo, tab_graficos, tab_processos, tab_historico = st.tabs([
    "Resumo",
    "Gráficos",
    "Processos",
    "Histórico"
])

# --- Aba Resumo ---
with tab_resumo:
    st.fragment(painel_resumo, run_every=intervalo)()

# --- Aba Histórico ---
# Fica antes da aba Gráficos no código para que o botão registre a medição
# antes de o gráfico ler o CSV. Na tela, a ordem das abas continua a mesma.
with tab_historico:
    st.subheader("Histórico de desempenho")

    if st.button("Registrar medição no histórico", type="primary"):
        dados, _, status_geral = obter_diagnostico()
        registrar_medicao(dados, status_geral)
        st.success("Medição registrada.")

    medicoes = ler_historico()

    # Usado pela aba Gráficos. Linhas corrompidas no CSV são ignoradas.
    dados_grafico = []

    for medicao in medicoes:
        try:
            dados_grafico.append({
                "Data e hora": medicao["data_hora"],
                "CPU": float(medicao["cpu"]),
                "RAM": float(medicao["ram"]),
                "Disco": float(medicao["disco"])
            })
        except (ValueError, TypeError, KeyError):
            continue

    if medicoes:
        icones = {"OK": "🟢", "ATENÇÃO": "🟡", "CRÍTICO": "🔴"}

        st.caption(
            f"{len(medicoes)} medições registradas. "
            "Abaixo, as 10 mais recentes, da mais recente para a mais antiga."
        )

        df_hist = pd.DataFrame(list(reversed(medicoes[-10:])))

        csv_historico = pd.DataFrame(medicoes).to_csv(
            index=False, sep=";"
        ).encode("utf-8-sig")

        st.download_button(
            "Baixar histórico completo (CSV)",
            data=csv_historico,
            file_name="historico_company_monitor.csv",
            mime="text/csv"
        )


        for coluna in ["cpu", "ram", "disco"]:
            df_hist[coluna] = pd.to_numeric(df_hist[coluna], errors="coerce")

        df_hist["internet"] = df_hist["internet"].map(
            {"True": "Online", "False": "Offline"}
        )
        df_hist["status_geral"] = df_hist["status_geral"].map(
            lambda s: f"{icones.get(s, '⚪')} {s}"
        )

        df_hist = df_hist[[
            "data_hora", "cpu", "ram", "disco", "internet", "status_geral"
        ]]
        df_hist.columns = [
            "Data e hora", "CPU", "RAM", "Disco", "Internet", "Status"
        ]

        st.dataframe(
            df_hist,
            hide_index=True,
            width="stretch",
            column_config={
                "CPU": st.column_config.ProgressColumn(
                    "CPU", format="%.1f%%", min_value=0, max_value=100
                ),
                "RAM": st.column_config.ProgressColumn(
                    "RAM", format="%.1f%%", min_value=0, max_value=100
                ),
                "Disco": st.column_config.ProgressColumn(
                    "Disco", format="%.1f%%", min_value=0, max_value=100
                ),
            },
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

        col_periodo, col_metricas = st.columns(2)

        with col_periodo:
            periodo = st.radio(
                "Período",
                ["Últimas 24 horas", "Últimos 7 dias", "Tudo"],
                index=2,
                horizontal=True
            )

        with col_metricas:
            metricas = st.multiselect(
                "Métricas",
                ["CPU", "RAM", "Disco"],
                default=["CPU", "RAM"]
            )

        if periodo == "Últimas 24 horas":
            df = df[df.index >= datetime.now() - pd.Timedelta(hours=24)]
        elif periodo == "Últimos 7 dias":
            df = df[df.index >= datetime.now() - pd.Timedelta(days=7)]

        if df.empty or not metricas:
            st.info("Nenhuma medição para os filtros escolhidos.")
        else:
            st.line_chart(df[metricas])

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
    st.fragment(painel_processos, run_every=intervalo)()