import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Controle Financeiro", layout="wide")

# 1. Cria a conexão com a planilha (Resolve o erro 'conn is not defined')
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("💰 Teste de Conexão")

# 2. Botão de teste direto no Streamlit
if st.button("Executar Teste de Gravação"):
    try:
        # Criamos um dado de exemplo
        df_teste = pd.DataFrame([{
            "Data": "2026-04-28",
            "Descrição": "Teste do Marcelo",
            "Valor": 50.00,
            "Tipo": "Despesa",
            "Categoria": "Outros"
        }])
        
        # Tenta ler os dados existentes e adicionar o novo
        dados_existentes = conn.read()
        df_atualizado = pd.concat([dados_existentes, df_teste], ignore_index=True)
        
        # Envia para a planilha
        conn.update(data=df_atualizado)
        st.success("✅ O teste funcionou! Verifique a sua Planilha do Google agora.")
    except Exception as e:
        st.error(f"❌ Erro no teste: {e}")
        st.info("Dica: Verifique se as credenciais JSON estão nos 'Secrets' do Streamlit Cloud.")

# 3. Carrega o seu visual antigo (HTML) abaixo para referência
with open("app_financeiro_completo.html", "r", encoding="utf-8") as f:
    st.components.v1.html(f.read(), height=800, scrolling=True)
