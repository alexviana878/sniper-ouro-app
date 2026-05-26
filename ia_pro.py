import streamlit as st
from datetime import datetime
import os

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Sniper Ouro IA EXTREME",
    page_icon="🎯",
    layout="centered"
)

# =========================================================
# LOGIN RESTRITO MASTER
# =========================================================
SENHA_CORRETA = "AlexMestre2026"

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align:center;color:#ef4444;'>🔒 SNIPER OURO IA EXTREME</h1>", unsafe_allow_html=True)
    senha = st.text_input("Digite sua chave master:", type="password")

    if st.button("ATIVAR SISTEMA"):
        if senha == SENHA_CORRETA:
            st.session_state.autenticado = True
            st.success("Sistema liberado.")
            st.rerun()
        else:
            st.error("Chave inválida.")
    st.stop()

# =========================================================
# CSS PREMIUM
# =========================================================
st.markdown("""
<style>
.stApp { background-color: #0d0e15; }
.main-card { border: 2px solid #a855f7; border-radius: 15px; padding: 15px; background-color: #111322; margin-bottom: 15px; box-shadow: 0 0 15px #a855f7; color: white; }
.green-card { border: 2px solid #00ff00; border-radius: 15px; padding: 15px; background-color: #111322; margin-bottom: 15px; box-shadow: 0 0 18px #00ff00; color: white; }
.red-card { border: 2px solid #ef4444; border-radius: 15px; padding: 15px; background-color: #111322; margin-bottom: 15px; box-shadow: 0 0 12px #ef4444; color: white; }
.gold-card { border: 2px solid #f59e0b; border-radius: 15px; padding: 15px; background-color: #111322; margin-top: 20px; box-shadow: 0 0 12px #f59e0b; color: white; }
.clock-card { border: 1px solid #00ff00; border-radius: 10px; padding: 10px; text-align: center; background-color: #111322; box-shadow: 0 0 8px #00ff00; margin-bottom: 15px; }
.manifesto-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 15px; margin-bottom: 15px; }
th, td { padding: 8px; text-align: left; border-bottom: 1px solid #30363d; color: white; }
th { background-color: #21262d; color: #f59e0b; }
h1,h2,h3,p,label { color: white !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMÓRIA AUXILIAR EM DISCO (FIRMADO PARA NÃO SUMIR)
# =========================================================
ARQUIVO_TXT = "historico_calculado.txt"

def salvar_vela_no_banco_fixo(valor):
    with open(ARQUIVO_TXT, "a") as f:
        f.write(f"{valor}\n")

def carregar_velas_do_banco_fixo():
    if not os.path.exists(ARQUIVO_TXT): return []
    velas = []
    with open(ARQUIVO_TXT, "r") as f:
        for linha in f:
            if linha.strip(): velas.append(float(linha.strip()))
    return velas

# =========================================================
# MEMÓRIA VIVA SESSÃO
# =========================================================
if "historico" not in st.session_state:
    st.session_state.historico = carregar_velas_do_banco_fixo()
if "banco_padroes" not in st.session_state: st.session_state.banco_padroes = []
if "distancia_rosa" not in st.session_state: st.session_state.distancia_rosa = 0
if "acertos" not in st.session_state: st.session_state.acertos = 0
if "erros" not in st.session_state: st.session_state.erros = 0
if "ultima_entrada" not in st.session_state: st.session_state.ultima_entrada = None

# RELÓGIO
agora = datetime.now()
minutos_pagantes = [2,5,8,10,12,15,18,20,22,25,28,30,32,35,38,40,42,45,48,50,52,55,58,0]
janela_ativa = agora.minute in minutos_pagantes

st.markdown(f"""
<div class="clock-card">
<h2 style='color:#00ff00 !important; margin:0;'>{agora.strftime("%H:%M:%S")}</h2>
<p style='color:#00ff00 !important; margin:0;'>{"⚠️ ZONA PAGANTE ATIVA" if janela_ativa else "MONITORANDO MERCADO"}</p>
</div>
""", unsafe_allow_html=True)

st.title("🎯 SNIPER OURO IA EXTREME")

with st.expander("🧠 DIRETRIZES DA MENTALIDADE SNIPER ELITE"):
    st.markdown("""
    <div class="manifesto-card">
    <p style='color:#f59e0b !important; font-weight:bold; font-size:16px; margin-top:0;'>🛡️ O OBJETIVO NÃO É ENTRAR MAIS. É ELIMINAR ENTRADAS RUINS.</p>
    <p style='font-size:14px; color:#c9d1d9;'>O sistema aprende continuamente. Quanto mais velas reais forem inseridas, mais o motor contextual melhora.</p>
    </div>
    """, unsafe_allow_html=True)

# FUNCTIONS MATEMÁTICAS
def classificar_vela(valor):
    if valor < 1.20: return "X"
    elif valor < 2.00: return "B"
    elif valor < 5.00: return "R"
    elif valor < 10.00: return "P"
    elif valor < 20.00: return "A"
    else: return "E"

def gerar_padrao(historico):
    if len(historico) < 4: return None
    return "-".join([classificar_vela(v) for v in historico[-4:]])

def salvar_padrao(padrao, resultado):
    st.session_state.banco_padroes.append({"padrao": padrao, "resultado": resultado})

def recalcular_matriz_total():
    st.session_state.banco_padroes = []
    total = len(st.session_state.historico)
    if total >= 5:
        aux = []
        for idx, valor in enumerate(st.session_state.historico):
            dist = total - idx
            if dist <= 200: peso = 4
            elif dist <= 800: peso = 2
            else: peso = 1
            
            if len(aux) >= 4:
                pad = gerar_padrao(aux)
                if pad:
                    for _ in range(peso): salvar_padrao(pad, valor)
            aux.append(valor)

# IMPORTAÇÃO CSV
st.markdown('<div class="main-card">### 📂 TREINAR INTELIGÊNCIA</div>', unsafe_allow_html=True)
arquivo = st.file_uploader("Envie CSV/TXT com 1 vela por linha:", type=["csv", "txt"])

if arquivo is not None and len(st.session_state.historico) == 0:
    linhas = arquivo.read().decode("utf-8").splitlines()
    for linha in linhas:
        try:
            limpo = linha.strip()
            if not limpo: continue
            v_num = float(limpo.replace(",", "."))
            st.session_state.historico.append(v_num)
            salvar_vela_no_banco_fixo(v_num)
        except: pass
    recalcular_matriz_total()
    st.success("🔥 Inteligência Alimentada!")
    st.rerun()

def analisar_padroes():
    memoria = {}
    for registro in st.session_state.banco_padroes:
        padrao = registro["padrao"]
        resultado = registro["resultado"]
        if padrao not in memoria:
            memoria[padrao] = {"total": 0, "roxa": 0, "rosa": 0, "erro": 0}
        memoria[padrao]["total"] += 1
        if resultado >= 2.0: memoria[padrao]["roxa"] += 1
        else: memoria[padrao]["erro"] += 1
        if resultado >= 10.0: memoria[padrao]["rosa"] += 1
    return memoria

def calcular_score(historico, taxa_roxa, taxa_rosa, ocorrencias):
    score = 0
    if len(historico) < 4: return 0
    ultimas4 = historico[-4:]
    azuis = sum(1 for x in ultimas4 if x < 2.0)
    extremos = sum(1 for x in ultimas4 if x < 1.20)
    v_atual = historico[-1]

    if azuis >= 4: score -= 10
    if extremos >= 2: score -= 8
    if v_atual < 1.10: score -= 10
    if taxa_roxa >= 70: score += 5
    if taxa_roxa >= 80: score += 3
    if taxa_roxa >= 90: score += 4
    if taxa_rosa >= 15: score += 3
    if ocorrencias >= 3: score += 3
    if ocorrencias >= 8: score += 4
    if ocorrencias >= 20: score += 4
    if janela_ativa: score += 2
    if st.session_state.distancia_rosa >= 12: score += 2
    if len(historico) >= 2 and historico[-2] >= 2.0: score += 2
    if ultimas4[-1] < 2.0 and ultimas4[-2] >= 2.0 and azuis <= 2: score += 3
    return score

def processar_sinal(historico):
    if len(historico) < 20:
        return "ANALISANDO...", "red-card", f"ALIMENTE MAIS O SISTEMA ({len(historico)}/20)", "---", None

    padrao = gerar_padrao(historico)
    memoria = analisar_padroes()
    taxa_roxa, taxa_rosa, ocorrencias = 0.0, 0.0, 0

    if padrao in memoria:
        dados = memoria[padrao]
        ocorrencias = dados["total"]
        if ocorrencias > 0:
            taxa_roxa = (dados["roxa"] / ocorrencias) * 100
            taxa_rosa = (dados["rosa"] / ocorrencias) * 100

    if ocorrencias < 3:
        return "🚫 ZONA PROIBIDA", "red-card", f"PADRÃO ISOLADO ({padrao})", "---", None
    if taxa_roxa < 70:
        return "🚫 SEM FORÇA", "red-card", f"TAXA HISTÓRICA BAIXA ({taxa_roxa:.1f}%)", "---", None

    score = calcular_score(historico, taxa_roxa, taxa_rosa, ocorrencias)
    if score < 10:
        return "🚫 SCORE BAIXO", "red-card", f"SCORE ATUAL: {score}", "---", None

    if score >= 18:
        return f"💎 ENTRADA EXTREMA ({padrao})", "green-card", f"ROXA {taxa_roxa:.1f}% | ROSA {taxa_rosa:.1f}% | SCORE {score}", "99%", "ROXA"
    if score >= 12:
        return f"⚡ ENTRADA SNIPER ({padrao})", "main-card", f"ROXA {taxa_roxa:.1f}% | SCORE {score}", "92%", "ROXA"
    if taxa_rosa >= 25 and st.session_state.distancia_rosa >= 10:
        return f"🌸 BUSCAR ROSA ({padrao})", "green-card", f"CHANCE ROSA {taxa_rosa:.1f}%", "94%", "ROSA"
    
    return "AGUARDAR ✋", "red-card", f"SEM CONFLUÊNCIA (SCORE {score})", "---", None

# =========================================================
# ENTRADA MANUAL REAL-TIME (BLOCOS COESOS)
# =========================================================
st.markdown("<br>", unsafe_allow_html=True)
banca = st.number_input("Banca Inicial (R$):", min_value=0.0, value=20.0, step=1.0)
vela = st.number_input("Digite a última vela:", min_value=0.0, format="%.2f", step=0.01)

if st.button("CALCULAR PROBABILIDADE"):
    if st.session_state.ultima_entrada == "ROXA":
        if vela >= 2.0: st.session_state.acertos += 1
        else: st.session_state.erros += 1
    elif st.session_state.ultima_entrada == "ROSA":
        if vela >= 10.0: st.session_state.acertos += 1
        else: st.session_state.erros += 1

    if len(st.session_state.historico) >= 4:
        padrao_gerado = gerar_padrao(st.session_state.historico)
        if padrao_gerado: salvar_padrao(padrao_gerado, vela)

    st.session_state.historico.append(vela)
    salvar_vela_no_banco_fixo(vela)

    if vela >= 10.0: st.session_state.distancia_rosa = 0
    else: st.session_state.distancia_rosa += 1
    
    recalcular_matriz_total()
    st.rerun()

# EXECUÇÃO DO MOTOR APÓS TRATAMENTO DOS CLIQUES
sinal, cor, status, confianca, entrada_gerada = processar_sinal(st.session_state.historico)
st.session_state.ultima_entrada = entrada_gerada

# PAINEL PRINCIPAL
st.markdown(f"""
<div class="{cor}">
<h1 style='margin:0; color: {"#00ff00" if "ENTRADA" in sinal or "BUSCAR" in sinal else "#ef4444"} !important;'>{sinal}</h1>
<p style="margin:5px 0 0 0;"><b>CONFIANÇA:</b> {confianca}<br><b>DIRETRIZ:</b> {status}</p>
</div>
""", unsafe_allow_html=True)

# RADAR ROSA
st.markdown(f"""
<div class="main-card">
<h3>🌸 RADAR ROSA</h3>
<p style="margin:5px 0 0 0;">Distância atual: <b>{st.session_state.distancia_rosa}</b> rodadas sem alvo alto.</p>
</div>
""", unsafe_allow_html=True)

# PERFORMANCE
total_jogadas = st.session_state.acertos + st.session_state.erros
assertividade = (st.session_state.acertos / total_jogadas) * 100 if total_jogadas > 0 else 0

st.markdown("<div class='gold-card'><h3 style='text-align:center; color:#f59e0b !important; margin:0 0 10px 0;'>👑 PERFORMANCE DA IA</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1: st.metric("✅ ACERTOS", st.session_state.acertos)
with col2: st.metric("❌ ERROS", st.session_state.erros)
with col3: st.metric("📊 ASSERTIVIDADE", f"{assertividade:.1f}%")
st.markdown("</div>", unsafe_allow_html=True)

# TOP PADRÕES
st.markdown("<div class='main-card'><h3 style='text-align:center; color:#00ff00 !important; margin:0 0 15px 0;'>🏆 TOP PADRÕES</h3>", unsafe_allow_html=True)
memoria_mapeada = analisar_padroes()
ranking = []

for pad, dados in memoria_mapeada.items():
    if dados["total"] >= 3:
        taxa = (dados["roxa"] / dados["total"]) * 100
        ranking.append({"padrao": pad, "taxa": taxa, "total": dados["total"]})

ranking = sorted(ranking, key=lambda x: x["taxa"], reverse=True)[:5]

if ranking:
    for item in ranking:
        st.markdown(f"<p style='color:white; margin:5px 0;'>💎 <b>{item['padrao']}</b> → <span style='color:#00ff00;'>{item['taxa']:.1f}%</span> ({item['total']} ocorrências)</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='color:#888; text-align:center; margin:0;'>Aguardando padrões fortes.</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ÚLTIMAS VELAS
if len(st.session_state.historico) > 0:
    velas_texto = " → ".join([f"[{v}]" for v in st.session_state.historico[-15:]])
    st.markdown(f"<p style='color:#888; margin-top:15px;'><b>Últimas velas (Total em Memória Fixo: {len(st.session_state.historico)}):</b> {velas_texto}</p>", unsafe_allow_html=True)

# RESET TOTAL
st.markdown("<br>", unsafe_allow_html=True)
if st.button("REINICIAR SISTEMA"):
    if os.path.exists(ARQUIVO_TXT): os.remove(ARQUIVO_TXT)
    st.session_state.historico = []
    st.session_state.banco_padroes = []
    st.session_state.distancia_rosa = 0
    st.session_state.acertos = 0
    st.session_state.erros = 0
    st.session_state.ultima_entrada = None
    st.rerun()
