# 100% Gratuito - App de Sustentabilidade Ambiental (Rede Calábria) 🌿

Aplicativo interno desenvolvido em Python com **Streamlit** para automação de coleta, análise de faturas (via IA do Google Gemini) e geração de relatórios gerenciais focados no Eixo Ambiental para as unidades da Rede Calábria.

## 🛠️ Tecnologias Utilizadas
- **Front-end:** Streamlit
- **Hospedagem:** Hugging Face Spaces (Infraestrutura Gratuita)
- **Banco de Dados:** Google Sheets API
- **Inteligência Artificial:** Google Gemini 1.5/2.0 Flash (Cota Gratuita)

## 📋 Como funciona
1. O usuário entra no app e faz o upload da foto de uma conta de luz ou água.
2. O agente de IA lê a imagem, extrai o consumo (kWh ou m³) e o valor em R$.
3. Os dados são salvos automaticamente em uma planilha do Google Sheets.
4. O app gera gráficos em tempo real e um relatório em texto para a diretoria.
