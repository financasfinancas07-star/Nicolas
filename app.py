import streamlit as st
import pandas as pd

# Substitua pelo link da sua planilha
sheet_url = "https://docs.google.com/spreadsheets/d/1bUYJMbwVfXfcFb_hTWANCLwMhqWhp0DbAjKvhsDvArE/edit?usp=sharing"

# Ajuste o link para exportar como CSV
csv_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

# Lê os dados
df = pd.read_csv(csv_url)

st.write("Dados da Planilha:", df)
