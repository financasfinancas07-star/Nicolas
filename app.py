import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Configuração da página
st.set_page_config(page_title="Controle Financeiro", layout="wide")

# Conecta usando apenas o link dos Secrets (sem JSON/Private Key)
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("💰 Teste de Sincronização")

# Tente ler os dados
try:
    # Lendo especificamente a primeira aba
    df = conn.read(ttl=0) # ttl=0 força o app a buscar dados novos agora
    st.write("Conectado com sucesso! Abaixo estão os dados da planilha:")
    st.dataframe(df)
except Exception as e:
    st.error(f"Ainda há um problema: {e}")
