import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Configuração básica
st.set_page_config(page_title="Controle Financeiro", layout="wide")

# Conexão usando o link que está nos Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("💰 Teste de Sincronização")

try:
    # Lendo os dados da planilha pública
    # O ttl=0 faz o app buscar dados novos toda vez que você atualizar
    df = conn.read(ttl=0)
    
    if df.empty:
        st.warning("A planilha está vazia, mas a conexão funcionou!")
    else:
        st.success("✅ Conectado com sucesso!")
        st.dataframe(df) # Mostra a tabela com 'data', 'descricao', etc.

except Exception as e:
    st.error(f"Erro ao ler a planilha: {e}")
