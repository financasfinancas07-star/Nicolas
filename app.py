import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Gestão Financeira Familiar", layout="wide")

# Conectar ao Google Sheets (usando os Secrets que você já configurou)
conn = st.connection("gsheets", type=GSheetsConnection)

# Lendo o seu arquivo HTML
with open("app_financeiro_completo.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Exibindo o HTML na tela
components.html(html_content, height=1000, scrolling=True)

# --- PARTE NOVA PARA SALVAR OS DADOS ---
# Como o HTML é isolado, precisamos de um pequeno formulário Streamlit abaixo 
# ou integrar via query params. Para não complicar seu design agora, 
# vamos garantir que a conexão está ativa:

try:
    # Isso lê os dados da planilha para garantir que a conexão funciona
    df = conn.read()
    # st.write("Conectado à planilha!") # Remova o comentário (#) para testar se aparece no app
except Exception as e:
    st.error(f"Erro na conexão: {e}")
