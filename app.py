import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import json

# Configuração da página
st.set_page_config(page_title="Gestão Financeira Familiar", layout="wide", initial_sidebar_state="collapsed")

# Conectar ao Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para salvar dados
def salvar_dados(tipo, desc, valor, categoria="Outros", data=""):
    try:
        # Lê os dados atuais
        df_existente = conn.read()
        
        # Cria a nova linha
        nova_linha = pd.DataFrame([{
            "Data": data if data else pd.Timestamp.now().strftime("%Y-%m-%d"),
            "Tipo": tipo,
            "Descricao": desc,
            "Valor": float(valor),
            "Categoria": categoria
        }])
        
        # Junta e salva
        df_atualizado = pd.concat([df_existente, nova_linha], ignore_index=True)
        conn.update(data=df_atualizado)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        return False

# Ler o arquivo HTML
with open("app_financeiro_completo.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Renderiza o HTML
# Adicionamos um listener para capturar cliques do seu HTML
components.html(html_content, height=800, scrolling=True)

# Interface Streamlit Invisível para Processamento (Opcional se quiser botões nativos)
with st.expander("Lançamento Rápido (Backup)"):
    with st.form("form_lançamento"):
        col1, col2, col3 = st.columns(3)
        tipo = col1.selectbox("Tipo", ["Despesa", "Receita"])
        desc = col2.text_input("Descrição")
        valor = col3.number_input("Valor", min_value=0.0, step=0.01)
        
        if st.form_submit_button("Salvar na Planilha"):
            if desc and valor > 0:
                if salvar_dados(tipo, desc, valor):
                    st.success("Dados salvos com sucesso!")
                    st.balloons()
