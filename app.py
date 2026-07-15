import streamlit as st
import pandas as pd
import plotly.express as px
import os
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Rede Calábria Ambiental", layout="wide")
st.title("🌿 Portal de Sustentabilidade Ambiental")
st.subheader("Rede Calábria — Painel de Gestão")

# O PULO DO GATO: Se o Render tiver a variável de ambiente, nós forçamos o Streamlit a lê-la
spreadsheet_url = os.environ.get("CONNECTIONS_GSHEETS_SPREADSHEET")

if spreadsheet_url:
    # Injeta a URL diretamente na configuração interna do Streamlit antes de conectar
    st.secrets["connections"] = {"gsheets": {"spreadsheet": spreadsheet_url}}

try:
    # Agora a conexão é feita de forma segura
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_energia = conn.read(worksheet="energia", ttl=0)
    
    st.success("Conectado ao Banco de Dados com sucesso!")
    
    if not df_energia.empty:
        fig_ener = px.line(df_energia, x="mes_referencia", y="consumo_kwh", color="unidade", title="Consumo de Energia (kWh)")
        st.plotly_chart(fig_ener, use_container_width=True)
    else:
        st.info("Nenhum dado de energia registrado para exibir nos gráficos.")
        
except Exception as e:
    st.info("Aguardando configuração das variáveis de ambiente...")
    st.caption(f"Status detalhado do erro: {e}")
