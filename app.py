import streamlit as st
from streamlit_gsheets import GSheetsConnection

# 1. Cria a conexão usando o link dos Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Lê os dados (especifique o nome da aba se necessário, ex: worksheet="Página1")
df = conn.read()

# 3. Mostra os dados na tela para testar
st.write("### Dados Sincronizados:", df)
