import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import json

# Configuração da página para ocupar a tela toda
st.set_page_config(page_title="Controle Financeiro", layout="wide")

# Estabelece conexão com o Google Sheets (configurado no seu TOML/Secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FUNÇÃO PARA SALVAR NA PLANILHA ---
def salvar_no_google_sheets(json_dados):
    try:
        # Transforma o texto vindo do HTML em dicionário Python
        dados = json.loads(json_dados)
        
        # Lê os dados atuais da planilha (sem cache para vir o mais recente)
        df_atual = conn.read(ttl=0)
        
        # Cria uma nova linha com os dados recebidos
        nova_linha = pd.DataFrame([{
            "data": dados.get("date"),
            "descricao": dados.get("desc"),
            "valor": dados.get("val"),
            "categoria": dados.get("cat", "Geral"),
            "tipo": dados.get("tipo")
        }])
        
        # Junta o novo dado com os antigos e envia para a nuvem
        df_final = pd.concat([df_atual, nova_linha], ignore_index=True)
        conn.update(data=df_final)
        
        st.toast("✅ Sincronizado com o Google Sheets!", icon="☁️")
        return True
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        return False

# --- INTERFACE ---
st.title("Gestão Financeira Sincronizada")

# Tenta carregar o seu arquivo HTML (app_financeiro_completo.html)[cite: 1]
try:
    with open("app_financeiro_completo.html", "r", encoding="utf-8") as f:
        html_code = f.read()

    # Exibe o HTML e captura o retorno do 'postMessage' feito no JavaScript[cite: 1]
    # O valor retornado aqui é o que você enviou na função enviarParaStreamlit()[cite: 1]
    dados_recebidos = st.components.v1.html(html_code, height=750, scrolling=True)

    # Se houve um novo lançamento no HTML, o Streamlit processa o salvamento[cite: 1]
    if dados_recebidos:
        if salvar_no_google_sheets(dados_recebidos):
            # Recarrega o app para limpar o componente e atualizar a visualização
            st.rerun()

except FileNotFoundError:
    st.error("Erro: O arquivo 'app_financeiro_completo.html' não foi encontrado no GitHub!")

# --- VISUALIZAÇÃO DOS DADOS REAIS ---
st.write("---")
st.subheader("📊 Histórico Gravado na Nuvem")
df_nuvem = conn.read(ttl=0)

if not df_nuvem.empty:
    # Mostra os registros mais novos primeiro
    st.dataframe(df_nuvem.sort_index(ascending=False), use_container_width=True)
else:
    st.info("Nenhum dado encontrado na sua planilha do Google.")
