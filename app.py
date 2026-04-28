import streamlit as st
import streamlit.components.v1 as components

# Configuração da página para aproveitar bem o espaço
st.set_page_config(page_title="Gestão Financeira Familiar", layout="wide")

# Lendo o seu arquivo HTML exatamente como você o criou
with open("app_financeiro_completo.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Exibindo o HTML na tela
components.html(html_content, height=1000, scrolling=True)