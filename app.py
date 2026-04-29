# No seu app.py, modifique essa parte:
if dados_janela:
    try:
        dados_dict = json.loads(dados_janela)
        # Só tenta salvar se houver um valor real
        if dados_dict.get("val"): 
            if salvar_no_google_sheets(dados_dict):
                # LIMPA a variável global para o celular não enviar em loop
                streamlit_js_eval(js_expressions="window.dados_financeiros = null; window.parent.dados_financeiros = null;", want_output=False)
                st.success("Dados enviados!")
                st.rerun()
    except Exception as e:
        st.error(f"Erro no processamento: {e}")
