import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Rede Calábria Ambiental", layout="wide")
st.title("🌿 Painel de Sustentabilidade Ambiental")

# Conecta diretamente à planilha usando o novo conector do Streamlit
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Lê os dados da aba "energia"
    df_energia = conn.read(worksheet="energia")
    
    st.success("Conectado com sucesso à planilha da Rede Calábria!")
    st.write("### Dados Atuais de Energia", df_energia)

except Exception as e:
    st.info("Aguardando a configuração do link da planilha nos Secrets...")
