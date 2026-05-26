import streamlit as st
from datetime import datetime
import json
import os

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Sniper Ouro IA Adaptive",
    page_icon="🎯",
    layout="centered"
)

# =========================================================
# LOGIN MASTER
# =========================================================
SENHA_CORRETA = "AlexMestre2026"

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align:center;color:#ef4444;'>🔒 SNIPER OURO IA ADAPTIVE</h1>", unsafe_allow_html=True)
    senha = st.text_input("Digite sua chave master:", type="password")
    if st.button("ATIVAR SISTEMA"):
        if senha == SENHA_CORRETA:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Senha inválida.")
    st.stop()

# =========================================================
# CSS PREMIUM
# =========================================================
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

# =========================================================
# ARQUIVO DE MEMÓRIA JSON
# =========================================================
ARQUIVO_MEMORIA = "memoria_sniper.json"

def carregar_memoria():
    if os.path.exists(ARQUIVO_MEMORIA):
        try:
            with open(ARQUIVO_MEMORIA, "r") as f:
                return json.load(f)
        except: pass
    return {
        "historico": [],
        "banco_padroes": [],
        "distancia_rosa": 0,
        "acertos": 0,
        "erros": 0,
        "ultimos_resultados": [],
        "bloqueados": {}
    }

def salvar_memoria():
    dados = {
        "historico": st.session_state.historico,
        "banco_padroes": st.session_state.banco_padroes,
        "distancia_rosa": st.session_state.distancia_rosa,
        "acertos": st.session_state.acertos,
        "erros": st.session_state.erros,
        "ultimos_resultados": st.session_state.ultimos_resultados,
        "bloqueados": st.session_state.bloqueados
    }
    with open(ARQUIVO_MEMORIA, "w") as f:
        json.dump(dados, f)

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

# RELÓGIO
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

# MATEMÁTICA DO MOTOR
def classificar_vela(valor):
    if valor < 1.20: return "X"
    elif valor < 2.00: return "B"
    elif valor < 5.00: return "R"
    elif valor < 10.00: return "P"
    elif valor < 20.00: return "A"
    return "E"

def gerar_padrao(historico):
    if len(historico) < 5: return None
    return "-".join([classificar_vela(v) for v in historico[-5:]])

def salvar_padrao(padrao, resultado):
    st.session_state.banco_padroes.append({"padrao": padrao, "resultado": resultado})

# =========================================================
# IMPORTAÇÃO CSV
# =========================================================
st.markdown('<div class="main-card"><h3>📂 TREINAR INTELIGÊNCIA VIVA</h3></div>', unsafe_allow_html=True)
arquivo = st.file_uploader("Envie CSV/TXT com 1 vela por linha", type=["csv","txt"], key="uploader_adaptive")

if arquivo is not None and len(st.session_state.historico) == 0:
    linhas = arquivo.read().decode("utf-8").splitlines()
    contador = 0
    for linha in linhas:
        try:
            valor = float(linha.strip().replace(",", "."))
            if len(st.session_state.historico) >= 5:
                padrao = gerar_padrao(st.session_state.historico)
                salvar_padrao(padrao, valor)
            st.session_state.historico.append(valor)
            if valor >= 10: st.session_state.distancia_rosa = 0
            else: st.session_state.distancia_rosa += 1
            contador += 1
        except: pass
    salvar_memoria()
    st.success(f"🔥 Sucesso: {contador} velas injetadas na V2!")
    st.rerun()

def analisar_padroes():
    memoria = {}
    for registro in st.session_state.banco_padroes:
        padrao = registro["padrao"]
        resultado = registro["resultado"]
        if padrao not in memoria:
            memoria[padrao] = {"total": 0, "roxa": 0, "rosa": 0}
        memoria[padrao]["total"] += 1
        if resultado >= 2: memoria[padrao]["roxa"] += 1
        if resultado >= 10: memoria[padrao]["rosa"] += 1
    return memoria

def calcular_score(historico, taxa_roxa, taxa_rosa, ocorrencias):
    score = 0
    ultimas5 = historico[-5:] if len(historico) >= 5 else historico
    azuis = sum(1 for x in ultimas5 if x < 2)
    extremos = sum(1 for x in ultimas5 if x < 1.20)

    if taxa_roxa >= 70: score += 4
    if taxa_roxa >= 80: score += 4
    if taxa_roxa >= 90: score += 5
    if taxa_rosa >= 20: score += 3

    if ocorrencias >= 5: score += 3
    if ocorrencias >= 15: score += 3

    if janela_ativa: score += 2
    if st.session_state.distancia_rosa >= 10: score += 2

    if azuis >= 4: score -= 8
    if extremos >= 2: score -= 5

    if len(st.session_state.ultimos_resultados) >= 3:
        erros = st.session_state.ultimos_resultados[-3:].count("LOSS")
        if erros >= 2: score -= 6
    return score

def processar_sinal(historico):
    if len(historico) < 30:
        return ("ANALISANDO...", "red-card", f"Sistema coletando dados ({len(historico)}/30)", "---", None)

    padrao = gerar_padrao(historico)
    memoria = analisar_padroes()
    taxa_roxa, taxa_rosa, ocorrencias = 0, 0, 0

    if padrao in memoria:
        dados = memoria[padrao]
        ocorrencias = dados["total"]
        taxa_roxa = (dados["roxa"] / ocorrencias) * 100
        taxa_rosa = (dados["rosa"] / ocorrencias) * 100

    if padrao in st.session_state.bloqueados:
        if st.session_state.bloqueados[padrao] >= 2:
            return ("🚫 PADRÃO BLOQUEADO (ESFRIOU)", "red-card", "Padrão retido temporariamente por proteção", "---", None)

    if ocorrencias < 5:
        return ("🚫 POUCA AMOSTRAGEM", "red-card", f"{ocorrencias} ocorrências em base", "---", None)

    if taxa_roxa < 70:
        return ("🚫 SEM FORÇA ESTATÍSTICA", "red-card", f"Taxa de acerto recente baixa ({taxa_roxa:.1f}%)", "---", None)

    score = calcular_score(historico, taxa_roxa, taxa_rosa, ocorrencias)

    if score < 12:
        return ("🚫 SCORE ADAPTATIVO BAIXO", "red-card", f"Score atual: {score}/12 mínimo", "---", None)

    if score >= 20:
        return (f"💎 ENTRADA EXTREMA ({padrao})", "green-card", f"ROXA {taxa_roxa:.1f}% | SCORE {score}", "99%", "ROXA")
    if score >= 14:
        return (f"⚡ ENTRADA SNIPER ({padrao})", "main-card", f"ROXA {taxa_roxa:.1f}% | SCORE {score}", "92%", "ROXA")
    if taxa_rosa >= 25 and st.session_state.distancia_rosa >= 10:
        return (f"🌸 BUSCAR ROSA ({padrao})", "green-card", f"CHANCE ROSA {taxa_rosa:.1f}%", "94%", "ROSA")

    return ("AGUARDAR ✋", "red-card", "Sem confluência contextual", "---", None)

# EXECUÇÃO DO MOTOR LÓGICO
sinal, cor, status, confianca, entrada = processar_sinal(st.session_state.historico)
st.session_state.ultima_entrada = entrada
st.session_state.padr_disparado = gerar_padrao(st.session_state.historico)

# =========================================================
# INTERFACE EXIBIDA CONTINUAMENTE (INPUTS DESBLOQUEADOS)
# =========================================================
st.markdown("<br>", unsafe_allow_html=True)
vela = st.number_input("Digite a última vela:", min_value=0.0, format="%.2f", step=0.01)

if st.button("CALCULAR PROBABILIDADE"):
    padr_avaliado = st.session_state.padr_disparado
    if st.session_state.ultima_entrada in ["ROXA", "ROSA"] and padr_avaliado:
        is_win = (st.session_state.ultima_entrada == "ROXA" and vela >= 2) or \
                 (st.session_state.ultima_entrada == "ROSA" and vela >= 10)
        if is_win:
            st.session_state.acertos += 1
            st.session_state.ultimos_resultados.append("WIN")
            if padr_avaliado in st.session_state.bloqueados:
                st.session_state.bloqueados[padr_avaliado] = max(0, st.session_state.bloqueados[padr_avaliado] - 1)
        else:
            st.session_state.erros += 1
            st.session_state.ultimos_resultados.append("LOSS")
            if padr_avaliado not in st.session_state.bloqueados: st.session_state.bloqueados[padr_avaliado] = 0
            st.session_state.bloqueados[padr_avaliado] += 1

    if len(st.session_state.historico) >= 5:
        padrao_atual = gerar_padrao(st.session_state.historico)
        salvar_padrao(padrao_atual, vela)

    st.session_state.historico.append(vela)
    if vela >= 10: st.session_state.distancia_rosa = 0
    else: st.session_state.distancia_rosa += 1

    salvar_memoria()
    st.rerun()

# PAINEL PRINCIPAL DO SINAL
st.markdown(f"""
<div class="{cor}">
<h1>{sinal}</h1>
<p><b>CONFIANÇA:</b> {confianca}<br><b>STATUS:</b> {status}</p>
</div>
""", unsafe_allow_html=True)

# PERFORMANCE DA IA
total = st.session_state.acertos + st.session_state.erros
assertividade = (st.session_state.acertos / total) * 100 if total > 0 else 0

st.markdown("""
<div class="gold-card">
<h3 style="text-align:center;">👑 PERFORMANCE DA IA PERSISTENTE</h3>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.metric("✅ ACERTOS", st.session_state.acertos)
with c2: st.metric("❌ ERROS", st.session_state.erros)
with c3: st.metric("📊 ASSERTIVIDADE", f"{assertividade:.1f}%")

# TOP PADRÕES
st.markdown("""
<div class="main-card">
<h3>🏆 TOP 5 PADRÕES DO MERCADO</h3>
</div>
""", unsafe_allow_html=True)

memoria_mapeada = analisar_padroes()
ranking = []

for pad, dados in memoria_mapeada.items():
    if dados["total"] >= 5:
        taxa = (dados["roxa"] / dados["total"]) * 100
        ranking.append({"padrao": pad, "taxa": taxa, "total": dados["total"]})
ranking = sorted(ranking, key=lambda x: x["taxa"], reverse=True)[:5]

if ranking:
    for item in ranking:
        st.markdown(f"""
        <div class="main-card">
        💎 <b>{item["padrao"]}</b><br>
        Taxa: <b>{item["taxa"]:.1f}%</b> | Ocorrências: <b>{item["total"]}</b>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("<p style='color:#888; text-align:center;'>Aguardando alimentação de dados estatísticos...</p>", unsafe_allow_html=True)

# ÚLTIMAS VELAS OPER
