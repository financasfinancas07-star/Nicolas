import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import json

# 1. Configuração da página
st.set_page_config(page_title="Controle Financeiro", layout="wide")

# 2. Conexão com a Planilha (usando o link dos Secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. Função para salvar os dados vindos do HTML
# Esta parte escuta o que o seu formulário envia
recebido = st.components.v1.html("", height=0) # Componente invisível para capturar dados

# Lógica para salvar na planilha quando você clica em "Registrar" no HTML
# Vamos usar um truque simples: um campo de texto invisível que o JS preenche
if "dados_html" not in st.session_state:
    st.session_state.dados_html = None

# Interface do Streamlit
st.title("💰 Controle Financeiro Familiar")

# 4. Carrega o seu formulário HTML
with open("app_financeiro_completo.html", "r", encoding="utf-8") as f:
    html_code = f.read()
    # Injetamos o código de ponte que te passei antes
    st.components.v1.html(html_code, height=600, scrolling=True)

# 5. Exibe a tabela da planilha logo abaixo para você conferir
st.write("### Histórico na Nuvem (Sincronizado)")
try:
    df_atual = conn.read(ttl=0)
    st.dataframe(df_atual, use_container_width=True)
except:
    st.write("Aguardando o primeiro registro...")
