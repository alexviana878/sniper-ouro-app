import streamlit as st
from datetime import datetime
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import brain

st.set_page_config(page_title="Sniper Ouro Ecossistema IA", page_icon="🎯", layout="centered")

SENHA_CORRETA = "AlexMestre2026"
if "autenticado" not in st.session_state: st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align:center;color:#ef4444;'>🔒 ECOSSISTEMA SNIPER IA</h1>", unsafe_allow_html=True)
    senha = st.text_input("Digite sua chave master:", type="password")
    if st.button("ATIVAR ECOSSISTEMA"):
        if senha == SENHA_CORRETA:
            st.session_state.autenticado = True
            st.rerun()
        else: st.error("Senha inválida.")
    st.stop()

st.markdown("""
<style>
.stApp { background-color: #0d1117; }
.main-card { border: 2px solid #7c3aed; border-radius: 15px; padding: 15px; background-color: #111827; margin-bottom: 15px; box-shadow: 0 0 12px #7c3aed; color: white; }
.green-card { border: 2px solid #00ff66; border-radius: 15px; padding: 15px; background-color: #111827; margin-bottom: 15px; box-shadow: 0 0 15px #00ff66; color: white; }
.red-card { border: 2px solid #ef4444; border-radius: 15px; padding: 15px; background-color: #111827; margin-bottom: 15px; box-shadow: 0 0 12px #ef4444; color: white; }
.gold-card { border: 2px solid #f59e0b; border-radius: 15px; padding: 15px; background-color: #111827; margin-bottom: 15px; box-shadow: 0 0 12px #f59e0b; color: white; }
.blue-card { border: 2px solid #3b82f6; border-radius: 15px; padding: 15px; background-color: #111827; margin-bottom: 15px; box-shadow: 0 0 12px #3b82f6; color: white; }
.clock-card { border: 1px solid #00ff66; border-radius: 10px; padding: 10px; background-color: #111827; text-align: center; margin-bottom: 15px; }
h1,h2,h3,p,label { color: white !important; }
</style>
""", unsafe_allow_html=True)

ARQUIVO_MEMORIA = "memoria_sniper.json"

def carregar_memoria():
    if os.path.exists(ARQUIVO_MEMORIA):
        try:
            with open(ARQUIVO_MEMORIA, "r") as f: return json.load(f)
        except: pass
    # ⚠️ GARGALO 3: ADICIONADA A ESTRUTURA DA MEMÓRIA NEGATIVA INICIAL
    return {"historico": [], "banco_padroes": [], "distancia_rosa": 0, "acertos": 0, "erros": 0, "ultimos_resultados": [], "quarentena": {}, "memoria_positiva": [], "memoria_negativa": {}}

def salvar_memoria():
    dados = {
        "historico": st.session_state.historico, 
        "banco_padroes": st.session_state.banco_padroes, 
        "distancia_rosa": st.session_state.distancia_rosa, 
        "acertos": st.session_state.acertos, 
        "erros": st.session_state.erros, 
        "ultimos_resultados": st.session_state.ultimos_resultados, 
        "quarentena": st.session_state.quarentena,
        "memoria_positiva": st.session_state.memoria_positiva,
        # Persiste a memória negativa das cicatrizes
        "memoria_negativa": st.session_state.memoria_negativa
    }
    with open(ARQUIVO_MEMORIA, "w") as f: json.dump(dados, f)

if "dados_carregados" not in st.session_state:
    dados = carregar_memoria()
    st.session_state.historico = dados.get("historico", [])
    st.session_state.banco_padroes = dados.get("banco_padroes", [])
    st.session_state.distancia_rosa = dados.get("distancia_rosa", 0)
    st.session_state.acertos = dados.get("acertos", 0)
    st.session_state.erros = dados.get("erros", 0)
    st.session_state.ultimos_resultados = dados.get("ultimos_resultados", [])
    st.session_state.quarentena = dados.get("quarentena", {})
    st.session_state.memoria_positiva = dados.get("memoria_positiva", [])
    # Carrega os estados da memória negativa
    st.session_state.memoria_negativa = dados.get("memoria_negativa", {})
    st.session_state.ultima_entrada = None
    st.session_state.ultimo_contexto = None
    st.session_state.dados_carregados = True

if st.session_state.quarentena:
    nova_quarentena = {}
    for ctx, rodadas in st.session_state.quarentena.items():
        decaimento = 3 if "ROSA" in ctx else 2
        nova = rodadas - decaimento
        if nova > 0: nova_quarentena[ctx] = nova
    st.session_state.quarentena = nova_quarentena

agora = datetime.now()
minutos_pagantes = [2,5,8,10,12,15,18,20,22,25,28,30,32,35,38,40,42,45,48,50,52,55,58,0]
janela_ativa = agora.minute in minutos_pagantes

st.markdown(f'<div class="clock-card"><h2 style="color:#00ff66 !important;margin:0;">{agora.strftime("%H:%M:%S")}</h2><p style="margin:0;color:#00ff66 !important;">{"⚠️ JANELA ATIVA DE EXPLOSÃO" if janela_ativa else "ECOSSISTEMA MONITORANDO"}</p></div>', unsafe_allow_html=True)

st.title("🎯 SNIPER OURO IA ADAPTIVE V2")

# RETORNADO PARA CARGA ÚNICA ULTRAESTÁVEL (Previne loops visuais na tela)
with st.expander("📂 RE-ABASTECER INTELIGÊNCIA CENTRAL (10.003 RODADAS)", expanded=False):
    arquivo = st.file_uploader("Suba a sua base viva completa", type=["csv","txt"])
    if arquivo is not None and len(st.session_state.historico) == 0:
        conteudo = arquivo.read().decode("utf-8")
        linhas = [ln.strip() for ln in conteudo.replace("\r", "\n").split("\n") if ln.strip()]
        novo_historico, novos_padroes, dist_rosa, contador = [], [], 0, 0
        for file_line in linhas:
            try:
                limpo = "".join([c for c in file_line if c.isdigit() or c in [".", ","]])
                if not limpo: continue
                valor = float(limpo.replace(",", "."))
                novo_historico.append(valor)
                dist_rosa = 0 if valor >= 10 else dist_rosa + 1
                contador += 1
            except: pass
        if len(novo_historico) >= 6:
            for i in range(5, len(novo_historico)):
                novos_padroes.append({"padrao": brain.gerar_padrao(novo_historico[i-5:i]), "resultado": novo_historico[i]})
        st.session_state.historico = novo_historico
        st.session_state.banco_padroes = novos_padroes
        st.session_state.distancia_rosa = dist_rosa
        salvar_memoria()
        st.success(f"🔥 Sincronizado: {contador} rodadas integradas!")
        st.rerun()

def analisar_banco():
    memoria = {}
    for reg in st.session_state.banco_padroes:
        pad = reg["padrao"]
        if pad not in memoria: memoria[pad] = {"total": 0, "roxa": 0, "rosa": 0}
        memoria[pad]["total"] += 1
        if reg["resultado"] >= 2: memoria[pad]["roxa"] += 1
        if reg["resultado"] >= 10: memoria[pad]["rosa"] += 1
    return memoria

if len(st.session_state.historico) >= 30:
    padrao_atual = brain.gerar_padrao(st.session_state.historico)
    fase_macro = brain.detectar_fase(st.session_state.historico)
    radar_score = brain.calcular_pressao_radar(st.session_state.historico, janela_ativa)
    expansion_score = brain.detectar_expansao(st.session_state.historico)
    
    banco = analisar_banco()
    
    historico_quente = st.session_state.historico[-120:]
    banco_quente = {}
    if len(historico_quente) >= 6:
        for i in range(5, len(historico_quente)):
            pad = brain.gerar_padrao(historico_quente[i-5:i])
            if pad:
                if pad not in banco_quente: banco_quente[pad] = {"total": 0, "roxa": 0, "rosa": 0}
                banco_quente[pad]["total"] += 1
                if historico_quente[i] >= 2: banco_quente[pad]["roxa"] += 1
                if historico_quente[i] >= 10: banco_quente[pad]["rosa"] += 1

    tx_roxa = tx_rosa = tx_roxa_quente = tx_rosa_quente = ocorrencias = ocorrencias_q = 0
    
    if padrao_atual in banco:
        dados_p = banco[padrao_atual]
        ocorrencias = dados_p["total"]
        tx_roxa = (dados_p["roxa"] / ocorrencias) * 100
        tx_rosa = (dados_p["rosa"] / ocorrencias) * 100
        
    if padrao_atual in banco_quente:
        dados_q = banco_quente[padrao_atual]
        ocorrencias_q = dados_q["total"]
        tx_roxa_quente = (dados_q["roxa"] / ocorrencias_q) * 100
        tx_rosa_quente = (dados_q["rosa"] / ocorrencias_q) * 100
        
    # ⚠️ GARGALO 2: AJUSTE IDEAL DE PESOS EQUILIBRADOS (55% HISTÓRICO VS 45% QUENTE)
    peso_historico, peso_quente = 0.55, 0.45
    tx_roxa_final = (tx_roxa * peso_historico) + (tx_roxa_quente * peso_quente)
    tx_rosa_final = (tx_rosa * peso_historico) + (tx_rosa_quente * peso_quente)
    
    adaptive_score = brain.calcular_score_adaptive(st.session_state.historico, tx_roxa_final, tx_rosa_final, ocorrencias, st.session_state.ultimos_resultados, janela_ativa)
    
    if st.session_state.distancia_rosa <= 5: faixa_rosa = "CURTA"
    elif st.session_state.distancia_rosa <= 12: faixa_rosa = "MEDIA"
    else: faixa_rosa = "LONGA"
    
    contexto_chave = f"{padrao_atual}_{fase_macro}_{faixa_rosa}"
    if contexto_chave in st.session_state.memoria_positiva:
        adaptive_score = min(adaptive_score + 8, 100)
        
    # ⚠️ GARGALO 1: APENAS O ADAPTIVE É PENALIZADO (Radar e Expansão removidos da punição)
    penalidade_quarentena = 0
    if contexto_chave in st.session_state.quarentena:
        rodadas_restantes = st.session_state.quarentena[contexto_chave]
        penalidade_quarentena = min(rodadas_restantes * 2, 30)
        
    adaptive_score = max(adaptive_score - penalidade_quarentena, 0)
    
    # ⚠️ GARGALO 3: APLICAÇÃO DA CICATRIZ DA MEMÓRIA NEGATIVA GRADUAL
    peso_cicatriz = st.session_state.memoria_negativa.get(contexto_chave, 0)
    adaptive_score -= min(peso_cicatriz * 1.5, 18)
    adaptive_score = max(adaptive_score, 0)
    
    mercado_instavel = tx_roxa_quente < 35 and radar_score < 45 and expansion_score < 45
    mercado_favoravel = tx_roxa_quente >= 55 and radar_score >= 60
    
    if mercado_favoravel: adaptive_score += 8
    if mercado_instavel: adaptive_score -= 12
    adaptive_score = max(min(adaptive_score, 100), 0)
    
    sinal_final, score_final = brain.calcular_consenso(adaptive_score, radar_score, expansion_score, fase_macro, tx_roxa_quente, mercado_instavel)
    st.session_state.ultima_entrada = sinal_final
    st.session_state.ultimo_contexto = contexto_chave
else:
    sinal_final, score_final, expansion_score, radar_score, fase_macro, ocorrencias, tx_roxa, tx_rosa, tx_roxa_quente, tx_rosa_quente, padrao_atual, adaptive_score = "COLETANDO DADOS", 0, 0, 0, "NEUTRA", 0, 0, 0, 0, 0, "---", 0

st.markdown('<div class="main-card"><h3>🎮 PAINEL DE COMANDO AO VIVO</h3></div>', unsafe_allow_html=True)
vela = st.number_input("Digite o resultado da última rodada:", min_value=0.0, format="%.2f", step=0.01)

if st.button("PROCESSAR E CALCULAR PROBABILIDADE"):
    if st.session_state.ultimo_contexto:
        sinal_ativo = st.session_state.ultima_entrada
        
        if "ROSA" in sinal_ativo:
            deu_green = vela >= 10
            is_rosa_signal = True
        else:
            deu_green = vela >= 2
            is_rosa_signal = False
            
        if ("ELITE" in sinal_ativo or "CHANCE" in sinal_ativo or "ROSA" in sinal_ativo):
            if not deu_green:
                tempo_quarentena = 10 if is_rosa_signal else 25
                st.session_state.quarentena[st.session_state.ultimo_contexto] = tempo_quarentena
                st.session_state.erros += 1
                st.session_state.ultimos_resultados.append("LOSS")
                
                # ⚠️ GARGALO 3: ADICIONA PESO DE CICATRIZ NA MEMÓRIA NEGATIVA DO CONTEXTO
                ctx_errado = st.session_state.ultimo_contexto
                if ctx_errado not in st.session_state.memoria_negativa: st.session_state.memoria_negativa[ctx_errado] = 0
                st.session_state.memoria_negativa[ctx_errado] += 1
            else:
                if len(st.session_state.memoria_positiva) >= 300: st.session_state.memoria_positiva.pop(0)
                if st.session_state.ultimo_contexto not in st.session_state.memoria_positiva: st.session_state.memoria_positiva.append(st.session_state.ultimo_contexto)
                st.session_state.acertos += 1
                st.session_state.ultimos_resultados.append("WIN")
                
        if len(st.session_state.ultimos_resultados) > 50: st.session_state.ultimos_resultados.pop(0)

    if len(st.session_state.historico) >= 5: st.session_state.banco_padroes.append({"padrao": brain.gerar_padrao(st.session_state.historico), "resultado": vela})
    st.session_state.historico.append(vela)
    st.session_state.distancia_rosa = 0 if vela >= 10 else st.session_state.distancia_rosa + 1
    salvar_memoria()
    st.write(f"Vela {vela} processada com sucesso!")
    st.rerun()

cor_card = "red-card"
if "ELITE" in sinal_final: cor_card = "green-card"
elif "CHANCE" in sinal_final: cor_card = "main-card"
elif "ROSA" in sinal_final: cor_card = "blue-card"
elif "OBSERVANDO" in sinal_final: cor_card = "gold-card"

st.markdown(f'<div class="{cor_card}"><h1 style="text-align:center;font-size:38px;margin:0;">{sinal_final}</h1><p style="text-align:center;margin:5px 0 0 0;font-size:18px;"><b>FORÇA DO CONSENSO IA:</b> {score_final}% | <b>PADRÃO ATUAL:</b> {padrao_atual}</p></div>', unsafe_allow_html=True)

st.markdown('<div class="main-card"><h3>🧠 STATUS DA BANCA MULTICÉREBRO</h3></div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**🛡️ Cérebro Defensivo (Fase Macro):** {fase_macro}")
    st.markdown(f"**⚡ Radar Rosa (Micro Pressão):** {radar_score}%")
    st.markdown(f"**📊 Ocorrências Mapeadas (Total):** {ocorrencias}")
    st.markdown(f"**📉 Taxa Roxa Global:** {tx_roxa:.1f}%")
    st.markdown(f"**🔥 Taxa Roxa Quente:** {tx_roxa_quente:.1f}%")
with col2:
    st.markdown(f"**🌸 Cérebro de Expansão (Alvo Rosa):** {expansion_score}%")
    st.markdown(f"**🧬 Força Base (Core Adaptive):** {adaptive_score}%")
    st.markdown(f"**🌸 Taxa Rosa Global:** {tx_rosa:.1f}%")
    st.markdown(f"**🌸 Taxa Rosa Quente:** {tx_rosa_quente:.1f}%")
    st.markdown(f"**⏱️ Distância da Última Rosa:** {st.session_state.distancia_rosa} rodadas")

if len(st.session_state.historico) > 0:
    st.markdown('<div class="main-card"><h3>📊 MONITOR DE FLUXO EM TEMPO REAL</h3></div>', unsafe_allow_html=True)
    ultimas_velas = st.session_state.historico[-16:]
    velas_texto = " → ".join([f"**[{v}]**" for v in ultimas_velas])
    st.markdown(f"<p style='font-size:18px;color:#00ff66;line-height:1.6;'>{velas_texto}</p>", unsafe_allow_html=True)

if st.session_state.memoria_positiva:
    with st.expander(f"🌟 MEMÓRIA POSITIVA ATIVA ({len(st.session_state.memoria_positiva)}/300 PADRÕES ATIVOS)", expanded=False):
        for ctx in st.session_state.memoria_positiva[-10:]:
            st.markdown(f"💎 **Contexto Composto:** `{ctx}` (+8% Score bônus)")

if st.session_state.quarentena:
    st.markdown('<div class="blue-card"><h3>❄️ CONTEXTOS EM QUARENTENA ATIVA (PENALIDADE GRADUAL)</h3></div>', unsafe_allow_html=True)
    for ctx, rds in st.session_state.quarentena.items():
        peso_penalidade = min(rds * 2, 30)
        st.write(f"🚫 **Geladeira:** `{ctx}` → Restam **{rds}** rodadas (Penalidade Ativa: -{peso_penalidade}%)")

total = st.session_state.acertos + st.session_state.erros
assertividade = (st.session_state.acertos / total) * 100 if total > 0 else 0
st.markdown('<div class="gold-card"><h3 style="text-align:center;">👑 PERFORMANCE GLOBAL MULTICAMADAS</h3></div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.metric("✅ GREEN ACERTOS", st.session_state.acertos)
with c2: st.metric("❌ REDS COLETADOS", st.session_state.erros)
with c3: st.metric("📊 ASSERTIVIDADE LÍQUIDA", f"{assertividade:.1f}%")

st.markdown(f"<p style='color:#666;text-align:center;font-size:12px;'>Base Total Ativa: {len(st.session_state.historico)} rodadas.</p>", unsafe_allow_html=True)

if st.button("RESETAR ECOSSISTEMA TOTAL"):
    if os.path.exists(ARQUIVO_MEMORIA): os.remove(ARQUIVO_MEMORIA)
    st.session_state.historico, st.session_state.banco_padroes, st.session_state.distancia_rosa, st.session_state.acertos, st.session_state.erros, st.session_state.ultimos_resultados, st.session_state.quarentena, st.session_state.memoria_positiva, st.session_state.memoria_negativa = [], [], 0, 0, 0, [], {}, [], {}
    st.session_state.ultima_entrada = None
    st.session_state.ultimo_contexto = None
    salvar_memoria()
    st.rerun()
