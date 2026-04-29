import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_js_eval import streamlit_js_eval
import pandas as pd
import json

st.set_page_config(page_title="Controle Financeiro", layout="wide")

conn = st.connection("gsheets", type=GSheetsConnection)

def salvar_no_google_sheets(dados_dict):
    try:
        df_atual = conn.read(ttl=0)
        
        nova_linha = pd.DataFrame([{
            "data": dados_dict.get("date"),
            "descricao": dados_dict.get("desc"),
            "valor": dados_dict.get("val"),
            "categoria": dados_dict.get("cat", "Geral"),
            "tipo": dados_dict.get("tipo")
        }])
        
        df_final = pd.concat([df_atual, nova_linha], ignore_index=True)
        conn.update(data=df_final)
        st.toast("✅ Sincronizado com o Google!", icon="☁️")
        return True
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        return False

# --- CAPTURA DE DADOS ---
# Usamos o componente comum para mostrar o HTML
with open("app_financeiro_completo.html", "r", encoding="utf-8") as f:
    html_code = f.read()

st.components.v1.html(html_code, height=750, scrolling=True)

# Esta função "escuta" o que o JavaScript envia via postMessage
# Ela resolve o erro de 'deltagenerator' porque espera o dado real
dados_janela = streamlit_js_eval(js_expressions="window.dados_financeiros", want_output=True)

if dados_janela:
    st.write(f"Depuração: O Python recebeu isso do celular: {dados_janela}") #
    # Se o dado chegou, salvamos e limpamos a variável para não duplicar
    if salvar_no_google_sheets(json.loads(dados_janela)):
        streamlit_js_eval(js_expressions="window.dados_financeiros = null", want_output=False)
        st.rerun()

st.write("---")
st.subheader("📊 Histórico na Nuvem")
st.dataframe(conn.read(ttl=0).sort_index(ascending=False), use_container_width=True)
