import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Controle Financeiro", layout="wide")

# Conexão com a planilha
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("💰 Controle Financeiro Familiar")

# Botão de teste para validar a sincronização
if st.button("Executar Teste de Gravação"):
    try:
        df_teste = pd.DataFrame([{
            "data": "2026-04-28",
            "descricao": "Teste Sincronismo",
            "valor": 22.00,
            "categoria": "Outros",
            "tipo": "Despesa"
        }])
        
        # Lê os dados da planilha 'Página1'
        dados_existentes = conn.read(worksheet="Página1")
        df_atualizado = pd.concat([dados_existentes, df_teste], ignore_index=True)
        
        # Atualiza a planilha no Google Drive
        conn.update(worksheet="Página1", data=df_atualizado)
        st.success("✅ Gravado na Planilha! Verifique no telemóvel agora.")
    except Exception as e:
        st.error(f"Erro: {e}")

# Carrega o seu HTML abaixo
with open("app_financeiro_completo.html", "r", encoding="utf-8") as f:
    st.components.v1.html(f.read(), height=800, scrolling=True)
