if arquivo is not None and len(st.session_state.historico) == 0:
        conteudo = arquivo.read().decode("utf-8")
        linhas = [ln.strip() for ln in conteudo.replace("\r", "\n").split("\n")]
        dados_brutos = []
        for file_line in linhas:
            try:
                limpo = "".join([c for c in file_line if c.isdigit() or c in [".", ","]])
                if not limpo: 
                    # Se a linha estiver vazia ou inválida, insere 1.00 para manter a contagem exata da linha do Excel
                    dados_brutos.append(1.00)
                    continue
                dados_brutos.append(float(limpo.replace(",", ".")))
            except:
                dados_brutos.append(1.00) # Salvaguarda contra erros de formatação
            
        if bloco_opcao == "Bloco 1 (Velas 1 a 10.000)":
            novo_historico = dados_brutos[:10000]
            st.session_state.bloco_validacao = "BLOCO 1 (TREINO)"
        elif bloco_opcao == "Bloco 2 (Velas 10.001 a 15.000 - Fora da Amostra)":
            novo_historico = dados_brutos[10000:15000]
            st.session_state.bloco_validacao = "BLOCO 2 (OUT-OF-SAMPLE)"
        elif bloco_opcao == "Bloco 3 (Velas 15.001 a 20.000 - Fora da Amostra)":
            novo_historico = dados_brutos[15000:20000]
            st.session_state.bloco_validacao = "BLOCO 3 (OUT-OF-SAMPLE)"
        else:
            novo_historico = dados_brutos
            st.session_state.bloco_validacao = "COMPLETO"

        novos_padroes, dist_rosa = [], 0
        for i, valor in enumerate(novo_historico):
            dist_rosa = 0 if valor >= 10 else dist_rosa + 1
            if i >= 5:
                novos_padroes.append({"padrao": brain.gerar_padrao(novo_historico[i-5:i]), "resultado": valor})
                
        st.session_state.historico = novo_historico
        st.session_state.banco_padroes = novos_padroes
        st.session_state.distancia_rosa = dist_rosa
        salvar_memoria()
        st.success(f"🔥 Laboratório Carregado: {len(novo_historico)} rodadas ativadas na partição {st.session_state.bloco_validacao}!")
        st.rerun()
