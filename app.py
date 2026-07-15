import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# 1. Configuração de visualização da página
st.set_page_config(page_title="Rede Calábria Ambiental", layout="wide")
st.title("🌿 Portal de Sustentabilidade Ambiental")
st.subheader("Rede Calábria — Registo e Indicadores")

# 2. Conectar à Planilha de forma simplificada
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Ler dados das abas (com ttl=0 para obter os dados em tempo real sem cache prolongado)
    df_energia = conn.read(worksheet="energia", ttl=0)
    df_residuos = conn.read(worksheet="residuos", ttl=0)
    
    st.success("Conectado ao Banco de Dados (Google Sheets) com sucesso!")
    
    # Criar abas visuais na tela
    aba_dash, aba_registo = st.tabs(["📊 Painel de Desempenho", "📝 Registar Dados"])
    
    with aba_dash:
        st.write("### Indicadores Recentes")
        if not df_energia.empty:
            col1, col2 = st.columns(2)
            with col1:
                # Gráfico de Consumo de Energia ao longo do tempo
                fig_ener = px.line(df_energia, x="mes_referencia", y="consumo_kwh", color="unidade", title="Consumo de Energia (kWh)")
                st.plotly_chart(fig_ener, use_container_width=True)
            with col2:
                # Gráfico de custos
                fig_custo = px.bar(df_energia, x="mes_referencia", y="valor_pago", color="unidade", title="Gastos com Energia (R$)")
                st.plotly_chart(fig_custo, use_container_width=True)
        else:
            st.info("Nenhum dado de energia registado para exibir nos gráficos.")
            
    with aba_registo:
        st.write("### Registar Nova Fatura ou Medição")
        # Formulário manual simples (Enquanto criamos o agente de IA para ler faturas)
        with st.form("form_registo"):
            unidade = st.selectbox("Selecione a Unidade", ["Sede Operacional", "Calábria Centro", "Instituto São Lucas"])
            mes = st.selectbox("Mês de Referência", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
            ano = st.number_input("Ano", min_value=2024, max_value=2030, value=2026)
            consumo = st.number_input("Consumo (kWh)", min_value=0.0)
            valor = st.number_input("Valor Pago (R$)", min_value=0.0)
            
            submetido = st.form_submit_state = st.form_submit_button("Guardar Registo")
            
            if submetido:
                # Criar nova linha de dados
                novo_dado = pd.DataFrame([{
                    "id": f"{unidade.lower().replace(' ', '_')}_{ano}_{mes.lower()[:3]}",
                    "data_registro": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "unidade": unidade,
                    "mes_referencia": mes,
                    "ano_referencia": ano,
                    "consumo_kwh": consumo,
                    "valor_pago": valor
                }])
                
                # Juntar ao DataFrame atual e atualizar a planilha
                df_atualizado = pd.concat([df_energia, novo_dado], ignore_index=True)
                conn.update(worksheet="energia", data=df_atualizado)
                st.balloons()
                st.success("Registo adicionado diretamente na folha de cálculo!")

except Exception as e:
    st.info("Aguardando configuração dos segredos de conexão...")
    st.caption(f"Status do sistema: {e}")
