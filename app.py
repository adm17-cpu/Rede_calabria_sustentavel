import streamlit as st
import pandas as pd
import plotly.express as px
import os
from streamlit_gsheets import GSheetsConnection

# 1. Configuração de visualização da página
st.set_page_config(page_title="Rede Calábria Ambiental", layout="wide")
st.title("🌿 Portal de Sustentabilidade Ambiental")
st.subheader("Rede Calábria — Painel de Gestão")

# 2. Resgata a URL da planilha configurada no Render
spreadsheet_url = os.environ.get("CONNECTIONS_GSHEETS_SPREADSHEET")

# 3. Força a configuração do segredo antes de iniciar a conexão
if spreadsheet_url:
    # Usamos o método .update() para contornar o bloqueio de atribuição direta do Streamlit
    st.secrets.update({"connections": {"gsheets": {"spreadsheet": spreadsheet_url}}})

# 4. Tenta conectar e ler os dados
try:
    # A conexão agora lê a configuração injetada acima
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Lendo a aba "Energia" (conforme a sua planilha)
    df_energia = conn.read(worksheet="Energia", ttl=0)
    
    st.success("Conectado ao Banco de Dados com sucesso!")
    
    if not df_energia.empty:
        # Cria o gráfico interativo de linha
        fig_ener = px.line(df_energia, x="mes_referencia", y="consumo_kwh", color="unidade", title="Consumo de Energia (kWh)")
        st.plotly_chart(fig_ener, use_container_width=True)
    else:
        st.info("Nenhum dado de energia registrado para exibir nos gráficos.")
        
except Exception as e:
    st.error("Erro ao carregar os dados:")
    st.caption(f"Status do sistema: {e}")
