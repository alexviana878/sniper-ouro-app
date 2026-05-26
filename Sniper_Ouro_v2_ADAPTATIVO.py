import streamlit as st
from datetime import datetime
import os

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Sniper Ouro v2 Adaptativo",
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
    st.title("🔒 SNIPER OURO V2 ADAPTATIVO")
    senha = st.text_input("Digite sua chave:", type="password")
    if st.button("ENTRAR"):
        if senha == SENHA_CORRETA:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Senha incorreta")
    st.stop()

# =========================================================
# CSS PREMIUM
# =========================================================
st.markdown("""
<style>
.stApp { background-color: #0d1117; }
.green-card { border: 2px solid #00ff88; border-radius: 15px; padding: 20px; background-color: #111827; box-shadow: 0 0 15px #00ff88; margin-bottom: 15px; }
.red-card { border: 2px solid #ef4444; border-radius: 15px; padding: 20px; background-color: #111827; box-shadow: 0 0 15px #ef4444; margin-bottom: 15px; }
.blue-card { border: 2px solid #3b82f6; border-radius: 15px; padding: 20px; background-color: #111827; box-shadow: 0 0 15px #3b82f6; margin-bottom: 15px; }
.gold-card { border: 2px solid #f59e0b; border-radius: 15px; padding: 20px; background-color: #111827; box-shadow: 0 0 15px #f59e0b; margin-top: 20px; }
h1,h2,h3,p,label { color: white !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# GAVETA FIXA NO DISCO DA V2 (TOTALMENTE SEPARADA DA V1)
# =========================================================
ARQUIVO_TXT_V2 = "historico_v2_adaptativo.txt"

def salvar_vela_no_disco_v2(valor):
    with open(ARQUIVO_TXT_V2, "a") as f:
        f.write(f"{valor}\n")

def carregar_velas_do_disco_v2():
    if not os.path.exists(ARQUIVO_TXT_V2): return []
    velas = []
    with open(ARQUIVO_TXT_V2, "r") as f:
        for linha in f:
            if linha.strip(): velas.append(float(linha.strip()))
    return list(velas)

# =========================================================
# MEMÓRIA VIVA DA SESSÃO
# =========================================================
if "historico" not in st.session_state:
    st.session_state.historico = carregar_velas_do_disco_v2()

if "banco_padroes" not in st.session_state: st.session_state.banco_padroes = []
if "acertos" not in st.session_state: st.session_state.acertos = 0
if "erros" not in st.session_state: st.session_state.erros = 0
if "ultima_entrada" not in st.session_state: st.session_state.ultima_entrada = None
if "distancia_rosa" not in st.session_state: st.session_state.distancia_rosa = 0

# RELÓGIO
agora = datetime.now()
st.markdown(f"""
<div class="blue-card">
<h2 style="margin:0;">⏰ {agora.strftime("%H:%M:%S")}</h2>
<p style="margin:0;">MOTOR ADAPTATIVO ONLINE</p>
</div>
""", unsafe_allow_html=True)

st.title("🎯 SNIPER OURO V2 ADAPTATIVO")

# CLASSIFICAÇÃO
def classificar_vela(valor):
    if valor < 1.20: return "X"
    elif valor < 2.00: return "B"
    elif valor < 5.00: return "R"
    elif valor < 10.00: return "P"
    elif valor < 20.00: return "A"
    else: return "E"

def gerar_padrao(historico):
    if len(historico) < 5: return None
    return "-".join([classificar_vela(v) for v in historico[-5:]])

def salvar_padrao_v2(padrao, resultado, peso=1):
    st.session_state.banco_padroes.append({
        "padrao": padrao,
        "resultado": resultado,
        "peso": peso
    })

def recalcular_matriz_v2():
    st.session_state.banco_padroes = []
    total = len(st.session_state.historico)
    if total >= 6:
        aux = []
        for idx, valor in enumerate(st.session_state.historico):
            distancia = total - idx
            
            # MEMÓRIA ADAPTATIVA: Pesos 5, 3 e 1 baseados na proximidade
            if distancia <= 200: peso = 5
            elif distancia <= 1000: peso = 3
            else: peso = 1
            
            if len(aux) >= 5:
                pad = gerar_padrao(aux)
                if pad: salvar_padrao_v2(pad, valor, peso)
            aux.append(valor)

# Inicializa a matriz de padrões caso o arquivo já possua dados
if len(st.session_state.historico) > 0 and len(st.session_state.banco_padroes) == 0:
    recalcular_matriz_v2()

# =========================================================
# IMPORTAÇÃO CSV (BLINDADA)
# =========================================================
st.subheader("📂 TREINAR INTELIGÊNCIA")
arquivo = st.file_uploader("Envie CSV/TXT com 1 vela por linha", type=["csv", "txt"])

if arquivo is not None and len(st.session_state.historico) == 0:
    linhas = arquivo.read().decode("utf-8").splitlines()
    for linha in linhas:
        try:
            limpo = linha.strip()
            if not limpo: continue
            valor = float(limpo.replace(",", "."))
            st.session_state.historico.append(valor)
            salvar_vela_no_disco_v2(valor)
        except: pass
    recalcular_matriz_v2()
    st.success(f"{len(st.session_state.historico)} velas carregadas com sucesso!")
    st.rerun()

def analisar_padroes():
    memoria = {}
    for item in st.session_state.banco_padroes:
        padrao = item["padrao"]
        resultado = item["resultado"]
        peso = item["peso"]
        if padrao not in memoria:
            memoria[padrao] = {"total": 0, "roxa": 0, "rosa": 0}
        memoria[padrao]["total"] += peso
        if resultado >= 2: memoria[padrao]["roxa"] += peso
        if resultado >= 10: memoria[padrao]["rosa"] += peso
    return memoria

def calcular_score(historico, taxa_roxa, taxa_rosa, ocorrencias):
    score = 0
    if len(historico) < 5: return 0
    ultimas5 = historico[-5:]
    azuis = sum(1 for x in ultimas5 if x < 2)
    extremos = sum(1 for x in ultimas5 if x < 1.20)

    if azuis >= 4: score -= 10
    if extremos >= 2: score -= 8
    if historico[-1] < 1.10: score -= 10

    if taxa_roxa >= 70: score += 4
    if taxa_roxa >= 80: score += 4
    if taxa_roxa >= 90: score += 5
    if taxa_rosa >= 20: score += 3

    if ocorrencias >= 5: score += 3
    if ocorrencias >= 15: score += 4
    if ocorrencias >= 30: score += 5

    if st.session_state.distancia_rosa >= 10: score += 2
    if historico[-2] >= 2: score += 2

    if ultimas5[-1] < 2 and ultimas5[-2] >= 2 and azuis <= 2: score += 3
    return score

def processar_sinal(historico):
    if len(historico) < 30:
        return "ANALISANDO...", "red-card", "Sistema ainda coletando dados", "---", None

    memoria = analisar_padroes()
    padrao = gerar_padrao(historico)
    taxa_roxa, taxa_rosa, ocorrencias = 0, 0, 0

    if padrao in memoria:
        dados = memoria[padrao]
        ocorrencias = dados["total"]
        if ocorrencias > 0:
            taxa_roxa = (dados["roxa"] / ocorrencias) * 100
            taxa_rosa = (dados["rosa"] / ocorrencias) * 100

    if ocorrencias < 5:
        return "🚫 ZONA PROIBIDA", "red-card", f"Pouca recorrência ({ocorrencias})", "---", None
    if taxa_roxa < 70:
        return "🚫 SEM FORÇA", "red-card", f"Taxa baixa ({taxa_roxa:.1f}%)", "---", None

    score = calcular_score(historico, taxa_roxa, taxa_rosa, ocorrencias)

    if score < 12:
        return "🚫 AGUARDAR", "red-card", f"Score insuficiente ({score})", "---", None

    if score >= 20:
        return f"💎 ENTRADA EXTREMA ({padrao})", "green-card", f"ROXA {taxa_roxa:.1f}% | SCORE {score}", "99%", "ROXA"
    if score >= 14:
        return f"⚡ ENTRADA SNIPER ({padrao})", "blue-card", f"ROXA {taxa_roxa:.1f}% | SCORE {score}", "92%", "ROXA"
    if taxa_rosa >= 25 and st.session_state.distancia_rosa >= 10:
        return f"🌸 BUSCAR ROSA ({padrao})", "green-card", f"ROSA {taxa_rosa:.1f}%", "94%", "ROSA"

    return "AGUARDAR", "red-card", "Sem confluência", "---", None

# =========================================================
# ENTRADA MANUAL REAL-TIME
# =========================================================
vela = st.number_input("Digite a última vela", min_value=0.0, format="%.2f", step=0.01)

if st.button("CALCULAR"):
    if st.session_state.ultima_entrada == "ROXA":
        if vela >= 2: st.session_state.acertos += 1
        else: st.session_state.erros += 1
    elif st.session_state.ultima_entrada == "ROSA":
        if vela >= 10: st.session_state.acertos += 1
        else: st.session_state.erros += 1

    salvar_vela_no_disco_v2(vela)
    st.session_state.historico.append(vela)

    if len(st.session_state.historico) >= 6:
        hist_previo = st.session_state.historico[:-1]
        pad_man = gerar_padrao(hist_previo)
        if pad_man: salvar_padrao_v2(pad_man, vela, peso=3)

    if vela >= 10: st.session_state.distancia_rosa = 0
    else: st.session_state.distancia_rosa += 1
    st.rerun()

# CONTROLE DE FLUXO DE EXIBIÇÃO
sinal, cor, status, confianca, entrada = processar_sinal(st.session_state.historico)
st.session_state.ultima_entrada = entrada

# PAINEL PRINCIPAL
st.markdown(f"""
<div class="{cor}">
<h1>{sinal}</h1>
<p><b>STATUS:</b> {status}</p>
<p><b>CONFIANÇA:</b> {confianca}</p>
</div>
""", unsafe_allow_html=True)

# RADAR ROSA
st.markdown(f"""
<div class="blue-card">
<h3>🌸 RADAR ROSA</h3>
<p>{st.session_state.distancia_rosa} rodadas sem rosa</p>
</div>
""", unsafe_allow_html=True)

# PERFORMANCE
total = st.session_state.acertos + st.session_state.erros
assertividade = (st.session_state.acertos / total) * 100 if total > 0 else 0

st.markdown('<div class="gold-card"><h2>👑 PERFORMANCE</h2></div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1: st.metric("✅ ACERTOS", st.session_state.acertos)
with col2: st.metric("❌ ERROS", st.session_state.erros)
with col3: st.metric("📊 ASSERTIVIDADE", f"{assertividade:.1f}%")

# TOP PADRÕES
st.subheader("🏆 TOP PADRÕES")
ranking = []
memoria = analisar_padroes()

for padrao_ch, dados in memoria.items():
    if dados["total"] >= 5:
        taxa = (dados["roxa"] / dados["total"]) * 100
        ranking.append({"padrao": padrao_ch, "taxa": taxa, "total": dados["total"]})
ranking = sorted(ranking, key=lambda x: x["taxa"], reverse=True)[:5]

for item in ranking:
    st.write(f"💎 {item['padrao']} → {item['taxa']:.1f}% ({item['total']} ocorrências)")

# HISTÓRICO RECENTE
if len(st.session_state.historico) > 0:
    texto = " → ".join([f"[{v}]" for v in st.session_state.historico[-15:]])
    st.markdown(f"<p style='color:#888;'><b>Últimas velas (Total em Base Adaptativa: {len(st.session_state.historico)}):</b> {texto}</p>", unsafe_allow_html=True)

# RESET TOTAL EXCLUSIVO DA V2
if st.button("REINICIAR SISTEMA"):
    if os.path.exists(ARQUIVO_TXT_V2): os.remove(ARQUIVO_TXT_V2)
    st.session_state.historico = []
    st.session_state.banco_padroes = []
    st.session_state.acertos = 0
    st.session_state.erros = 0
    st.session_state.ultima_entrada = None
    st.session_state.distancia_rosa = 0
    st.rerun()
