import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Gestão Financeira Familiar", layout="wide")

# Lendo o seu arquivo HTML 
with open("app_financeiro_completo.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Exibindo o HTML na tela - Aumentei a altura para 1200
components.html(html_content, height=1200, scrolling=True)
