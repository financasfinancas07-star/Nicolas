import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Configuração da página
st.set_page_config(page_title="Gestão Financeira", layout="wide")

# 1. Conexão com a Planilha (usa os Secrets que você configurou)
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Título do App
st.title("💰 Controle Financeiro Familiar")

# 3. Formulário de Lançamento (Este aqui NÃO SOME os dados)
st.subheader("📝 Novo Lançamento")
with st.form("meu_formulario", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        data = st.date_input("Data")
        tipo = st.selectbox("Tipo", ["Despesa", "Receita"])
    with col2:
        descricao = st.text_input("Descrição", placeholder="Ex: Mercado, Combustível...")
        categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Saúde", "Lazer", "Casa", "Outros"])
    with col3:
        valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01)
        botao = st.form_submit_button("GRAVAR NA PLANILHA")

    if botao:
        if descricao and valor > 0:
            try:
                # Lê os dados que já existem
                df_antigo = conn.read()
                
                # Cria a nova linha
                nova_linha = pd.DataFrame([{
                    "Data": data.strftime("%d/%m/%Y"),
                    "Tipo": tipo,
                    "Descricao": descricao,
                    "Categoria": categoria,
                    "Valor": valor
                }])
                
                # Junta tudo e envia para o Google
                df_final = pd.concat([df_antigo, nova_linha], ignore_index=True)
                conn.update(data=df_final)
                
                st.success(f"Feito! R$ {valor} salvos na planilha.")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
        else:
            st.warning("Por favor, preencha a descrição e o valor.")

# 4. Visualização do que já foi salvo (Opcional)
if st.checkbox("Ver lançamentos da planilha"):
    dados_planilha = conn.read()
    st.dataframe(dados_planilha.tail(10))

# 5. O seu visual antigo (Opcional - ficará no final da página)
with st.expander("Ver Painel Visual Antigo"):
    with open("app_financeiro_completo.html", "r", encoding="utf-8") as f:
        st.components.v1.html(f.read(), height=600, scrolling=True)
