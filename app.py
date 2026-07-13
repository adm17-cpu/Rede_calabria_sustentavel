import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# 1. Configuração inicial da página do Streamlit
st.set_page_config(page_title="Rede Calábria - Sustentabilidade", layout="wide")
st.title("🌿 Painel de Sustentabilidade Ambiental")
st.subheader("Rede Calábria — Gestão de Indicadores")

# 2. Função para conectar ao Google Sheets (com cache para não estourar limite de requisições)
@st.cache_resource
def conectar_banco_dados():
    # Define os escopos necessários para ler e escrever na planilha e no Drive
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Busca as credenciais de forma segura que estarão salvas no Secrets do Streamlit/HuggingFace
    credenciais_dict = st.secrets["gcp_service_account"]
    credentials = Credentials.from_service_account_info(credenciais_dict, scopes=scopes)
    
    # Autentica o cliente do gspread
    client = gspread.authorize(credentials)
    return client

try:
    # Inicializa a conexão
    gc = conectar_banco_dados()
    
    # Abre a planilha pelo nome exato que criamos
    planilha = gc.open("Rede_Calabria_Sustentavel")
    
    st.success("Conexão com o Banco de Dados (Google Sheets) estabelecida com sucesso!")

    # 3. Exemplo de Leitura de Dados (Aba de Energia)
    aba_energia = planilha.worksheet("energia")
    dados_fatais = aba_energia.get_all_records()
    
    if dados_fatais:
        df_energia = pd.DataFrame(dados_fatais)
        st.write("### Histórico de Consumo de Energia", df_energia)
    else:
        st.info("A tabela de energia está pronta, mas ainda não possui registros inseridos.")

except Exception as e:
    st.error("Aguardando configuração das credenciais de acesso...")
    st.caption(f"Detalhe técnico: {e}")
