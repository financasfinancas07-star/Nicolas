import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Primeiro definimos a conexão (isso resolve o NameError)
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Depois carregamos a tua interface HTML
with open("app_financeiro_completo.html", "r", encoding="utf-8") as f:
    html_code = f.read()

st.components.v1.html(html_code, height=800, scrolling=True)

# 3. Opcional: Criar um botão no próprio Streamlit para testar a gravação
# (Já que o botão dentro do HTML ainda não consegue "falar" com o Python facilmente)
if st.button("Testar Gravação na Planilha"):
    df_teste = pd.DataFrame([{"Data": "2026-04-29", "Descrição": "Teste Streamlit", "Valor": 10.00}])
    conn.create(data=df_teste)
    st.success("Gravado com sucesso!")
