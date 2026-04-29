import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Conexão simplificada (Gratuita e sem JSON)
conn = st.connection("gsheets", type=GSheetsConnection)

# Comando para ler os dados
df = conn.read()

st.write("Dados da Planilha:", df)
