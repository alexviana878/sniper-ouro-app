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
    return {"historico": [], "banco_padroes": [], "distancia_rosa": 0, "acertos": 0, "erros": 0, "ultimos_resultados": [], "quarentena": {}, "memoria_positiva": []}

def salvar_memoria():
    dados = {
        "historico": st.session_state.historico, 
        "banco_padroes": st.session_state.banco_padroes, 
        "distancia_rosa": st.session_state.distancia_rosa, 
        "acertos": st.session_state.acertos, 
        "erros": st.session_state.erros, 
        "ultimos_resultados": st.session_state.ultimos_resultados, 
        "quarentena": st.session_state.quarentena,
        "memoria_positiva": st.session_state.memoria_positiva
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
    st.session_state.ultima_entrada = None
    st.session_state.ultimo_contexto = None
    st.session_state.dados_carregados = True

# Processa decaimento da Quarentena
if st.session_state.quarentena:
    nova_quarentena = {}
    for ctx, rodadas in st.session_state.quarentena.items():
        if rodadas > 1: nova_quarentena[ctx] = rodadas - 1
    st.session_state.quarentena = nova_quarentena

agora = datetime.now()
minutos_pagantes = [2,5,8,10,12,15,18,20,22,25,28,30,32,35,38,40,42,45,48,50,52,55,58,0]
janela_ativa = agora.minute in minutos_pagantes

st.markdown(f'<div class="clock-card"><h2 style="color:#00ff66 !important;margin:0;">{agora.strftime("%H:%M:%S")}</h2><p style="margin:0;color:#00ff66 !important;">{"⚠️ JANELA ATIVA DE EXPLOSÃO" if janela_ativa else "ECOSSISTEMA MONITORANDO"}</p></div>', unsafe_allow_html=True)

st.title("🎯 SNIPER OURO IA ADAPTIVE V2")

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
    tx_roxa, tx_rosa, ocorrencias = 0, 0, 0
    if padrao_atual in banco:
        dados_p = banco[padrao_atual]
        ocorrencias = dados_p["total"]
        tx_roxa = (dados_p["roxa"] / ocorrencias) * 100
        tx_rosa = (dados_p["rosa"] / ocorrencias) * 100
        
    adaptive_score = brain.calcular_score_adaptive(st.session_state.historico, tx_roxa, tx_rosa, ocorrencias, st.session_state.ultimos_resultados, janela_ativa)
    
    # Aplica bônus de Memória Positiva (Passo 4) se o contexto for historicamente vencedor
    contexto_chave = f"{padrao_atual}_{fase_macro}"
    if contexto_chave in st.session_state.memoria_positiva:
        adaptive_score = min(adaptive_score + 8, 100)
        
    bloqueado_quarentena = contexto_chave in st.session_state.quarentena
    
    sinal_final, score_final = brain.calcular_consenso(adaptive_score, radar_score, expansion_score, bloqueado_quarentena, fase_macro)
    st.session_state.ultima_entrada = sinal_final
    st.session_state.ultimo_contexto = contexto_chave
else:
    sinal_final, score_final, expansion_score, radar_score, fase_macro, ocorrencias, tx_roxa, padrao_atual, adaptive_score = "COLETANDO DADOS", 0, 0, 0, "NEUTRA", 0, 0, "---", 0

st.markdown('<div class="main-card"><h3>🎮 PAINEL DE COMANDO AO VIVO</h3></div>', unsafe_allow_html=True)
vela = st.number_input("Digite o resultado da última rodada:", min_value=0.0, format="%.2f", step=0.01)

if st.button("PROCESSAR E CALCULAR PROBABILIDADE"):
    if st.session_state.ultimo_contexto:
        sinal_ativo = st.session_state.ultima_entrada
        
        # GERENCIAMENTO INTELIGENTE DA MEMÓRIA DE ACERTOS E ERROS
        # GERENCIAMENTO INTELIGENTE DA MEMÓRIA DE ACERTOS E ERROS (CORRIGIDO)
        if "ROSA" in sinal_ativo:
            deu_green = vela >= 10
            is_rosa_signal = True
        else:
            deu_green = vela >= 2
            is_rosa_signal = False
            
        if ("ELITE" in sinal_ativo or "CHANCE" in sinal_ativo or "ROSA" in sinal_ativo):
            if not deu_green:
                # PASSO 3 REFINADO: Quarentena de 10 rodadas para Rosas e 25 rodadas para Roxas comuns
                tempo_quarentena = 10 if is_rosa_signal else 25
                st.session_state.quarentena[st.session_state.ultimo_contexto] = tempo_quarentena
                st.session_state.erros += 1
                st.session_state.ultimos_resultados.append("LOSS")
            else:
                # PASSO 4: REGISTRAR ACERTO NA MEMÓRIA POSITIVA
                if st.session_state.ultimo_contexto not in st.session_state.memoria_positiva:
                    st.session_state.memoria_positiva.append(st.session_state.ultimo_contexto)
                st.session_state.acertos += 1
                st.session_state.ultimos_resultados.append("WIN")
                
        elif "QUARENTENA" in sinal_ativo and deu_green:
            if st.session_state.ultimo_contexto in st.session_state.quarentena:
                del st.session_state.quarentena[st.session_state.ultimo_contexto]

    if len(st.session_state.historico) >= 5:
        st.session_state.banco_padroes.append({"padrao": brain.gerar_padrao(st.session_state.historico), "resultado": vela})
        
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
    st.markdown(f"**📊 Ocorrências Mapeadas:** {ocorrencias}")
with col2:
    st.markdown(f"**🌸 Cérebro de Expansão (Alvo Rosa):** {expansion_score}%")
    st.markdown(f"**🧬 Força Base (Core Adaptive):** {adaptive_score}%")
    st.markdown(f"**📉 Taxa Roxa Registrada:** {tx_roxa:.1f}%")

if len(st.session_state.historico) > 0:
    st.markdown('<div class="main-card"><h3>📊 MONITOR DE FLUXO EM TEMPO REAL</h3></div>', unsafe_allow_html=True)
    ultimas_velas = st.session_state.historico[-16:]
    velas_texto = " → ".join([f"**[{v}]**" for v in ultimas_velas])
    st.markdown(f"<p style='font-size:18px;color:#00ff66;line-height:1.6;'>{velas_texto}</p>", unsafe_allow_html=True)

# EXIBE A MEMÓRIA POSITIVA CONQUISTADA
if st.session_state.memoria_positiva:
    with st.expander("🌟 MEMÓRIA POSITIVA ATIVA (PADRÕES VENCEDORES COLETADOS)", expanded=False):
        for ctx in st.session_state.memoria_positiva:
            st.markdown(f"💎 **Contexto Consolidado:** `{ctx}` (+8% Score bônus)")

if st.session_state.quarentena:
    st.markdown('<div class="blue-card"><h3>❄️ CONTEXTOS EM QUARENTENA ATIVA (MEMÓRIA DE DOR)</h3></div>', unsafe_allow_html=True)
    for ctx, rds in st.session_state.quarentena.items():
        # Identifica visualmente o tipo de quarentena aplicada
        tipo_q = "ROSA" if "ROSA" in ctx or score_final == 0 else "ROXA"
        st.write(f"🚫 **Frio ({tipo_q}):** `{ctx}` → Congelado por mais **{rds}** rodadas.")

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
    st.session_state.historico, st.session_state.banco_padroes, st.session_state.distancia_rosa, st.session_state.acertos, st.session_state.erros, st.session_state.ultimos_resultados, st.session_state.quarentena, st.session_state.memoria_positiva = [], [], 0, 0, 0, [], {}, []
    salvar_memoria()
    st.rerun()
