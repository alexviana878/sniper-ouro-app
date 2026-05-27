import streamlit as st
from datetime import datetime
import json
import os
import brain  # CONEXÃO DIRETA COM O SEU NÚCLEO ISOLADO

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(page_title="Sniper Ouro IA Adaptive", page_icon="🎯", layout="centered")

# LOGIN MASTER
SENHA_CORRETA = "AlexMestre2026"
if "autenticado" not in st.session_state: st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align:center;color:#ef4444;'>🔒 SNIPER OURO IA ADAPTIVE</h1>", unsafe_allow_html=True)
    senha = st.text_input("Digite sua chave master:", type="password")
    if st.button("ATIVAR SISTEMA"):
        if senha == SENHA_CORRETA:
            st.session_state.autenticado = True
            st.rerun()
        else: st.error("Senha inválida.")
    st.stop()

# CSS PREMIUM
st.markdown("""
<style>
.stApp { background-color: #0d1117; }
.main-card { border: 2px solid #7c3aed; border-radius: 15px; padding: 15px; background-color: #111827; margin-bottom: 15px; box-shadow: 0 0 12px #7c3aed; color: white; }
.green-card { border: 2px solid #00ff66; border-radius: 15px; padding: 15px; background-color: #111827; margin-bottom: 15px; box-shadow: 0 0 15px #00ff66; color: white; }
.red-card { border: 2px solid #ef4444; border-radius: 15px; padding: 15px; background-color: #111827; margin-bottom: 15px; box-shadow: 0 0 12px #ef4444; color: white; }
.gold-card { border: 2px solid #f59e0b; border-radius: 15px; padding: 15px; background-color: #111827; margin-bottom: 15px; box-shadow: 0 0 12px #f59e0b; color: white; }
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
    return {"historico": [], "banco_padroes": [], "distancia_rosa": 0, "acertos": 0, "erros": 0, "ultimos_resultados": [], "bloqueados": {}}

def salvar_memoria():
    dados = {"historico": st.session_state.historico, "banco_padroes": st.session_state.banco_padroes, "distancia_rosa": st.session_state.distancia_rosa, "acertos": st.session_state.acertos, "erros": st.session_state.erros, "ultimos_resultados": st.session_state.ultimos_resultados, "bloqueados": st.session_state.bloqueados}
    with open(ARQUIVO_MEMORIA, "w") as f: json.dump(dados, f)

if "dados_carregados" not in st.session_state:
    dados = carregar_memoria()
    st.session_state.historico = dados.get("historico", [])
    st.session_state.banco_padroes = dados.get("banco_padroes", [])
    st.session_state.distancia_rosa = dados.get("distancia_rosa", 0)
    st.session_state.acertos = dados.get("acertos", 0)
    st.session_state.erros = dados.get("erros", 0)
    st.session_state.ultimos_resultados = dados.get("ultimos_resultados", [])
    st.session_state.bloqueados = dados.get("bloqueados", {})
    st.session_state.ultima_entrada = None
    st.session_state.padr_disparado = None
    st.session_state.dados_carregados = True

agora = datetime.now()
minutos_pagantes = [2,5,8,10,12,15,18,20,22,25,28,30,32,35,38,40,42,45,48,50,52,55,58,0]
janela_ativa = agora.minute in minutos_pagantes

st.markdown(f"""
<div class="clock-card">
<h2 style="color:#00ff66 !important;margin:0;">{agora.strftime("%H:%M:%S")}</h2>
<p style="margin:0;color:#00ff66 !important;">{"⚠️ ZONA PAGANTE" if janela_ativa else "MONITORANDO MERCADO"}</p>
</div>
""", unsafe_allow_html=True)

st.title("🎯 SNIPER OURO IA ADAPTIVE")

# IMPORTAÇÃO SUPER TURBO ULTRA ACELERADA
st.markdown('<div class="main-card"><h3>📂 TREINAR INTELIGÊNCIA VIVA</h3></div>', unsafe_allow_html=True)
arquivo = st.file_uploader("Envie CSV/TXT com 1 vela por linha", type=["csv","txt"], key="uploader_adaptive_turbo")

if arquivo is not None and len(st.session_state.historico) == 0:
    conteudo = arquivo.read().decode("utf-8")
    linhas = [ln.strip() for ln in conteudo.splitlines() if ln.strip()]
    
    novo_historico = []
    novos_padroes = []
    dist_rosa = 0
    contador = 0
    
    # Varre as linhas extraindo puramente os números de forma tolerante
    for file_line in linhas:
        try:
            # Remove caracteres invisíveis ou espaços extras da linha
            limpo = "".join([c for c in file_line if c.isdigit() or c in [".", ","]])
            if not limpo: continue
            valor = float(limpo.replace(",", "."))
            
            novo_historico.append(valor)
            if valor >= 10: dist_rosa = 0
            else: dist_rosa += 1
            contador += 1
        except: pass
        
    # Geração dos padrões em lote ultra rápida para economizar processamento
    if len(novo_historico) >= 6:
        for i in range(5, len(novo_historico)):
            # Pega fatias consecutivas para treinar a IA instantaneamente
            fatia = novo_historico[i-5:i]
            padr = brain.gerar_padrao(fatia)
            novos_padroes.append({"padrao": padr, "resultado": novo_historico[i]})

    st.session_state.historico = novo_historico
    st.session_state.banco_padroes = novos_padroes
    st.session_state.distancia_rosa = dist_rosa
    salvar_memoria()
    st.success(f"🔥 Sucesso: {contador} velas injetadas com processamento de alta performance!")
    st.rerun()

def analisar_padroes():
    memoria = {}
    for registro in st.session_state.banco_padroes:
        pad = registro["padrao"]
        res = registro["resultado"]
        if pad not in memoria: memoria[pad] = {"total": 0, "roxa": 0, "rosa": 0}
        memoria[pad]["total"] += 1
        if res >= 2: memoria[pad]["roxa"] += 1
        if res >= 10: memoria[pad]["rosa"] += 1
    return memoria

def processar_sinal(historico):
    if len(historico) < 30:
        return ("ANALISANDO...", "red-card", f"Sistema coletando dados ({len(historico)}/30)", "---", None, 0, "NEUTRA")

    padrao = brain.gerar_padrao(historico)
    memoria = analisar_padroes()
    taxa_roxa, taxa_rosa, ocorrencias = 0, 0, 0

    if padrao in memoria:
        dados = memoria[padrao]
        ocorrencias = dados["total"]
        taxa_roxa = (dados["roxa"] / ocorrencias) * 100
        taxa_rosa = (dados["rosa"] / ocorrencias) * 100

    if padrao in st.session_state.bloqueados:
        if st.session_state.bloqueados[padrao] >= 2:
            return ("🚫 PADRÃO BLOQUEADO (ESFRIOU)", "red-card", "Padrão retido temporariamente por proteção", "---", None, 0, "NEUTRA")

    if ocorrencias < 10:
        return ("🚫 POUCA AMOSTRAGEM", "red-card", f"Amostragem fraca ({ocorrencias} ocorrências). Mínimo exigido: 10.", "---", None, 0, "NEUTRA")

    if taxa_roxa < 70:
        return ("🚫 SEM FORÇA ESTATÍSTICA", "red-card", f"Taxa de acerto recente baixa ({taxa_roxa:.1f}%)", "---", None, 0, "NEUTRA")

    score = brain.calcular_score_adaptive(historico, taxa_roxa, taxa_rosa, ocorrencias, st.session_state.ultimos_resultados, janela_ativa)
    fase = brain.detectar_fase(historico)
    pressao_radar = brain.calcular_pressao_radar(historico, janela_ativa)

    if score >= 90: return (f"🔥 ENTRADA ELITE ({padrao})", "green-card", f"ROXA {taxa_roxa:.1f}% | SCORE {score}", "99%", "ROXA", pressao_radar, fase)
    if score >= 70: return (f"🟢 BOA CHANCE AGORA ({padrao})", "main-card", f"ROXA {taxa_roxa:.1f}% | SCORE {score}", "92%", "ROXA", pressao_radar, fase)
    if taxa_rosa >= 25 and st.session_state.distancia_rosa >= 10 and pressao_radar >= 60:
        return (f"🌸 BUSCAR ROSA ({padrao})", "green-card", f"CHANCE ROSA {taxa_rosa:.1f}% | PRESSÃO {pressao_radar}%", "94%", "ROSA", pressao_radar, fase)

    return ("AGUARDAR ✋", "red-card", f"Sem confluência contextual (Score: {score})", "---", None, pressao_radar, fase)

sinal, cor, status, confianca, entrada, pressao_radar_atual, fase_atual = processar_sinal(st.session_state.historico)
st.session_state.ultima_entrada = entrada
st.session_state.padr_disparado = brain.gerar_padrao(st.session_state.historico)

st.markdown("<br>", unsafe_allow_html=True)
vela = st.number_input("Digite a última vela:", min_value=0.0, format="%.2f", step=0.01)

if st.button("CALCULAR PROBABILIDADE"):
    padr_avaliado = st.session_state.padr_disparado
    if st.session_state.ultima_entrada in ["ROXA", "ROSA"] and padr_avaliado:
        is_win = (st.session_state.ultima_entrada == "ROXA" and vela >= 2) or (st.session_state.ultima_entrada == "ROSA" and vela >= 10)
        if is_win:
            st.session_state.acertos += 1
            st.session_state.ultimos_resultados.append("WIN")
            if padr_avaliado in st.session_state.bloqueados: st.session_state.bloqueados[padr_avaliado] = max(0, st.session_state.bloqueados[padr_avaliado] - 1)
        else:
            st.session_state.erros += 1
            st.session_state.ultimos_resultados.append("LOSS")
            if padr_avaliado not in st.session_state.bloqueados: st.session_state.bloqueados[padr_avaliado] = 0
            st.session_state.bloqueados[padr_avaliado] += 1

    if len(st.session_state.historico) >= 5:
        padrao_atual = brain.gerar_padrao(st.session_state.historico)
        st.session_state.banco_padroes.append({"padrao": padrao_atual, "resultado": vela})

    st.session_state.historico.append(vela)
    if vela >= 10: st.session_state.distancia_rosa = 0
    else: st.session_state.distancia_rosa += 1
    salvar_memoria()
    st.rerun()

st.markdown(f'<div class="{cor}"><h1>{sinal}</h1><p><b>CONFIANÇA ADAPTATIVA:</b> {confianca}<br><b>DIRETRIZ DE FLUXO:</b> {status}</p></div>', unsafe_allow_html=True)

# CAMADA DE PRESSÃO MICRO
cor_indicador = "#ef4444"
status_pressao = "NEUTRO"
if pressao_radar_atual >= 80: cor_indicador, status_pressao = "#00ff66", "JANELA ELITE 🔥"
elif pressao_radar_atual >= 60: cor_indicador, status_pressao = "#00ff66", "OPORTUNIDADE FORTE 🟢"
elif pressao_radar_atual >= 40: cor_indicador, status_pressao = "#f59e0b", "ATENÇÃO 🟡"

st.markdown(f"""
<div class="blue-card">
<h3>🌸 CAMADA MICRO: ÍNDICE DE PRESSÃO DO RADAR ROSA</h3>
<p style="font-size: 24px; color: {cor_indicador} !important; margin: 5px 0;"><b>{pressao_radar_atual}%</b> → {status_pressao}</p>
<p><b>Ciclo Corrente:</b> {st.session_state.distancia_rosa} rodadas consecutivas sem alvo alto. <b>Fase Macro:</b> {fase_atual}</p>
</div>
""", unsafe_allow_html=True)

total = st.session_state.acertos + st.session_state.erros
assertividade = (st.session_state.acertos / total) * 100 if total > 0 else 0

st.markdown('<div class="gold-card"><h3 style="text-align:center;">👑 PERFORMANCE DA IA PERSISTENTE ADAPTIVE</h3></div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.metric("✅ ACERTOS", st.session_state.acertos)
with c2: st.metric("❌ ERROS", st.session_state.erros)
with c3: st.metric("📊 ASSERTIVIDADE", f"{assertividade:.1f}%")

st.markdown('<div class="main-card"><h3>🏆 TOP 5 PADRÕES FILTRADOS (MÍNIMO 10 OCORRÊNCIAS)</h3></div>', unsafe_allow_html=True)
memoria_mapeada = analisar_padroes()
ranking = []
for pad, dados in memoria_mapeada.items():
    if dados["total"] >= 10:
        taxa = (dados["roxa"] / dados["total"]) * 100
        ranking.append({"padrao": pad, "taxa": taxa, "total": dados["total"]})
ranking = sorted(ranking, key=lambda x: x["taxa"], reverse=True)[:5]

if ranking:
    for item in ranking:
        st.markdown(f'<div class="main-card">💎 <b>{item["padrao"]}</b><br>Taxa: <b>{item["taxa"]:.1f}%</b> | Ocorrências: <b>{item["total"]}</b></div>', unsafe_allow_html=True)
else:
    st.markdown("<p style='color:#888; text-align:center;'>Buscando padrões sobreviventes com alta amostragem...</p>", unsafe_allow_html=True)

if len(st.session_state.historico) > 0:
    velas_texto = " → ".join([f"[{v}]" for v in st.session_state.historico[-15:]])
    st.markdown(f"<p style='color:#999;'><b>Últimas velas (Total na Base Viva: {len(st.session_state.historico)}):</b><br>{velas_texto}</p>", unsafe_allow_html=True)

if st.button("REINICIAR SISTEMA"):
    if os.path.exists(ARQUIVO_MEMORIA): os.remove(ARQUIVO_MEMORIA)
    st.session_state.historico, st.session_state.banco_padroes, st.session_state.distancia_rosa, st.session_state.acertos, st.session_state.erros, st.session_state.ultimos_resultados, st.session_state.bloqueados = [], [], 0, 0, 0, [], {}
    salvar_memoria()
    st.rerun()
