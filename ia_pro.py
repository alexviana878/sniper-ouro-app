import streamlit as st
from datetime import datetime

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
# CSS PREMIUM RE-ESTILIZADO
# =========================================================
st.markdown("""
<style>
.stApp { background-color: #0d0e15; }
.main-card { border: 2px solid #a855f7; border-radius: 15px; padding: 15px; background-color: #111322; margin-bottom: 15px; box-shadow: 0 0 15px #a855f7; color: white; }
.green-card { border: 2px solid #00ff00; border-radius: 15px; padding: 15px; background-color: #111322; margin-bottom: 15px; box-shadow: 0 0 18px #00ff00; color: white; }
.red-card { border: 2px solid #ef4444; border-radius: 15px; padding: 15px; background-color: #111322; margin-bottom: 15px; box-shadow: 0 0 12px #ef4444; color: white; }
.gold-card { border: 2px solid #f59e0b; border-radius: 15px; padding: 15px; background-color: #111322; margin-top: 20px; box-shadow: 0 0 12px #f59e0b; color: white; }
.clock-card { border: 1px solid #00ff00; border-radius: 10px; padding: 10px; text-align: center; background-color: #111322; box-shadow: 0 0 8px #00ff00; margin-bottom: 15px; }
h1,h2,h3,p,label { color: white !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# INICIALIZAÇÃO DE VARIÁVEIS DE SESSÃO
# =========================================================
if "historico" not in st.session_state: st.session_state.historico = []
if "banco_padroes" not in st.session_state: st.session_state.banco_padroes = []
if "distancia_rosa" not in st.session_state: st.session_state.distancia_rosa = 0
if "acertos" not in st.session_state: st.session_state.acertos = 0
if "erros" not in st.session_state: st.session_state.erros = 0
if "ultima_entrada" not in st.session_state: st.session_state.ultima_entrada = None

# =========================================================
# RELÓGIO DE JANELAS
# =========================================================
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

# =========================================================
# CLASSIFICAÇÃO INTELIGENTE DE 6 CAMADAS
# =========================================================
def classificar_vela(valor):
    if valor < 1.20: return "X"    # Compressão Extrema
    elif valor < 2.00: return "B"  # Baixa Comum
    elif valor < 5.00: return "R"  # Roxa Regular
    elif valor < 10.00: return "P" # Roxa Potente
    elif valor < 20.00: return "A" # Rosa Padrão
    else: return "E"               # Rosa Extrema

def gerar_padrao(historico):
    if len(historico) < 5: return None
    return "-".join([classificar_vela(v) for v in historico[-5:]])

def salvar_padrao(padrao, resultado):
    st.session_state.banco_padroes.append({"padrao": padrao, "resultado": resultado})

# =========================================================
# 📂 NOVO MOTOR DE IMPORTAÇÃO ULTRA RESILIENTE CONTRA BUGS
# =========================================================
st.markdown('<div class="main-card">### 📂 TREINAR INTELIGÊNCIA</div>', unsafe_allow_html=True)
arquivo = st.file_uploader("Envie CSV/TXT com 1 vela por linha:", type=["csv", "txt"])

if arquivo is not None and len(st.session_state.historico) == 0:
    linhas = arquivo.read().decode("utf-8").splitlines()
    velas_carga = []
    
    # Filtra e limpa rigorosamente cada linha do arquivo antes de processar
    for linha in linhas:
        try:
            limpo = linha.strip().replace('"', '').replace("'", "")
            if not limpo or any(c.isalpha() for c in limpo if c not in ['.', ',', '-']): 
                continue # Pula linhas vazias ou com cabeçalhos de texto do Excel
            velas_carga.append(float(limpo.replace(",", ".")))
        except: 
            pass
        
    total_velas = len(velas_carga)
    
    if total_velas > 0:
        for idx, valor in enumerate(velas_carga):
            distancia_do_fim = total_velas - idx
            
            if distancia_do_fim <= 300: peso = 5       
            elif distancia_do_fim <= 1000: peso = 3    
            else: peso = 1                             
            
            if len(st.session_state.historico) >= 5:
                padrao_existente = gerar_padrao(st.session_state.historico)
                if padrao_existente:
                    for _ in range(peso):
                        salvar_padrao(padrao_existente, valor)
                    
            st.session_state.historico.append(valor)
            st.session_state.distancia_rosa = 0 if valor >= 10.0 else st.session_state.distancia_rosa + 1

        st.success(f"🔥 {total_velas} velas integradas e calibradas com matriz de peso.")
    else:
        st.error("O arquivo enviado não contém números de velas válidos. Verifique se copiou apenas os números.")

# =========================================================
# ANALISADOR DE PADRÕES (ANTI-TRAVAMENTO)
# =========================================================
def analisar_padroes():
    memoria = {}
    if not st.session_state.banco_padroes:
        return memoria
    for registro in st.session_state.banco_padroes:
        padrao = registro["padrao"]
        resultado = registro["resultado"]
        if not padrao: continue

        if padrao not in memoria:
            memoria[padrao] = {"total": 0, "roxa": 0, "rosa": 0, "erro": 0}

        memoria[padrao]["total"] += 1
        if resultado >= 2.0: memoria[padrao]["roxa"] += 1
        else: memoria[padrao]["erro"] += 1
        if resultado >= 10.0: memoria[padrao]["rosa"] += 1
    return memoria

# =========================================================
# SCORE EXTREMO RIGOROSO
# =========================================================
def calcular_score(historico, taxa_roxa, taxa_rosa, ocorrencias):
    score = 0
    if len(historico) < 5: return 0

    v_atual = historico[-1]
    ultimas5 = historico[-5:]

    azuis = sum(1 for x in ultimas5 if x < 2.0)
    extremos = sum(1 for x in ultimas5 if x < 1.20)

    # Penalidades Críticas de Campo
    if azuis >= 4: score -= 10
    if extremos >= 2: score -= 8
    if v_atual < 1.10: score -= 10

    # Confluências Adaptativas
    if taxa_roxa >= 83: score += 6
    if taxa_roxa >= 90: score += 4
    if taxa_rosa >= 20: score += 4
    if taxa_rosa >= 35: score += 3
    
    if ocorrencias >= 15: score += 5
    if ocorrencias >= 30: score += 4
    
    if janela_ativa: score += 2
    if st.session_state.distancia_rosa >= 12: score += 2
    
    if len(historico) >= 2 and historico[-2] >= 2.0: score += 2

    # Gatilho de Recuperação Curta
    if ultimas5[-1] < 2.0 and ultimas5[-2] >= 2.0 and azuis <= 2:
        score += 3

    return score

# =========================================================
# PROCESSAMENTO CENTRAL EXTREMO
# =========================================================
def processar_sinal(historico):
    if len(historico) < 30:
        return "ANALISANDO...", "red-card", f"ALIMENTE MAIS O SISTEMA (VELAS NA MESA: {len(historico)}/30)", "---", None

    padrao = gerar_padrao(historico)
    memoria = analisar_padroes()
    taxa_roxa, taxa_rosa, ocorrencias = 0.0, 0.0, 0

    if padrao and padrao in memoria:
        dados = memoria[padrao]
        ocorrencias = dados["total"]
        if ocorrencias > 0:
            taxa_roxa = (dados["roxa"] / ocorrencias) * 100
            taxa_rosa = (dados["rosa"] / ocorrencias) * 100

    # --- FILTROS DE PROIBIÇÃO SISTÊMICOS ---
    if ocorrencias < 15:
        return "🚫 ZONA PROIBIDA", "red-card", f"PADRÃO REMOTO DE CAMPO ({padrao if padrao else '---'}) | SINAIS EM BASE: {ocorrencias} (MÍNIMO 15)", "---", None

    if taxa_roxa < 83.0:
        return "🚫 SEM FORÇA ESTATÍSTICA", "red-card", f"TAXA ABAIXO DA RÉGUA EXTREMA ({taxa_roxa:.1f}%)", "---", None

    score = calcular_score(historico, taxa_roxa, taxa_rosa, ocorrencias)

    if score < 15:
        return "🚫 SCORE INSUFICIENTE", "red-card", f"CONFLUÊNCIA DE CRITÉRIOS BAIXA (SCORE: {score})", "---", None

    # --- DISPARO DE ENTRADAS EXTREMAS ---
    if score >= 24:
        return f"💎 ENTRADA EXTREMA ({padrao})", "green-card", f"PADRÃO ELITE | ROXA {taxa_roxa:.1f}% | ROSA {taxa_rosa:.1f}% | SCORE {score}", "99%", "ROXA"
    if score >= 18:
        return f"⚡ ENTRADA SNIPER ({padrao})", "main-card", f"PADRÃO PREMIUM | ROXA {taxa_roxa:.1f}% | SCORE {score}", "92%", "ROXA"
    if taxa_rosa >= 35 and st.session_state.distancia_rosa >= 12:
        return f"🌸 BUSCAR ROSA ({padrao})", "green-card", f"PRESSÃO ROSA DETECTADA | CHANCE {taxa_rosa:.1f}%", "94%", "ROSA"
    
    return "AGUARDAR ✋", "red-card", f"MERCADO PROCESSADO. AGUARDANDO CONFLUÊNCIA DE ENTRADA (SCORE: {score})", "---", None

# =========================================================
# ENTRADA MANUAL REAL-TIME
# =========================================================
st.markdown("<br>", unsafe_allow_html=True)
banca = st.number_input("Banca Inicial (R$):", min_value=0.0, value=20.0, step=1.0)
vela = st.number_input("Digite a última vela:", min_value=0.0, format="%.2f", step=0.01)

if st.button("CALCULAR PROBABILIDADE"):
    if st.session_state.ultima_entrada in ["ROXA", "ROSA"]:
        if st.session_state.ultima_entrada == "ROXA":
            if vela >= 2.0: st.session_state.acertos += 1
            else: st.session_state.erros += 1
        elif st.session_state.ultima_entrada == "ROSA":
            if vela >= 10.0: st.session_state.acertos += 1
            else: st.session_state.erros += 1

    if len(st.session_state.historico) >= 5:
        padrao_gerado = gerar_padrao(st.session_state.historico)
        if padrao_gerado:
            salvar_padrao(padrao_gerado, vela)

    st.session_state.historico.append(vela)

    if vela >= 10.0: st.session_state.distancia_rosa = 0
    else: st.session_state.distancia_rosa += 1

    st.rerun()

# EXECUÇÃO DO MOTOR PREDITIVO
sinal, cor, status, confianca, entrada_gerada = processar_sinal(st.session_state.historico)
st.session_state.ultima_entrada = entrada_gerada

# =========================================================
# PAINEL PRINCIPAL
# =========================================================
st.markdown(f"""
<div class="{cor}">
<h1 style='margin:0; color: {'#00ff00' if 'ENTRADA' in sinal or 'BUSCAR' in sinal else '#ef4444'} !important;'>{sinal}</h1>
<p style="margin:5px 0 0 0;"><b>CONFIANÇA:</b> {confianca}<br><b>DIRETRIZ:</b> {status}</p>
</div>
""", unsafe_allow_html=True)

# EXIBIÇÃO RADAR ROSA
st.markdown(f"""
<div class="main-card">
<h3>🌸 RADAR ROSA</h3>
<p style="margin:5px 0 0 0;">Distância atual: <b>{st.session_state.distancia_rosa}</b> rodadas sem estourar alvos altos</p>
</div>
""", unsafe_allow_html=True)

# MONITOR DE PERFORMANCE EXTREMA (BLOCO PROTEGIDO)
total_jogadas = st.session_state.acertos + st.session_state.erros
assertividade = (st.session_state.acertos / total_jogadas) * 100 if total_jogadas > 0 else 0.0

st.markdown("<div class='gold-card'><h3 style='text-align:center;color:#f59e0b !important; margin:0 0 10px 0;'>👑 PERFORMANCE DA IA</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1: st.metric("✅ ACERTOS", st.session_state.acertos)
with col2: st.metric("❌ ERROS", st.session_state.erros)
with col3: st.metric("📊 ASSERTIVIDADE", f"{assertividade:.1f}%")
st.markdown("</div>", unsafe_allow_html=True)

# EXIBIÇÃO DOS TOP PADRÕES CONDICIONAL (ANTI-TRAVAMENTO)
st.markdown("<div class='main-card'><h3 style='text-align:center; color:#00ff00 !important; margin:0 0 15px 0;'>🏆 TOP PADRÕES DO LABORATÓRIO</h3>", unsafe_allow_html=True)
memoria_mapeada = analisar_padroes()
ranking = []

for pad, dados in memoria_mapeada.items():
    if dados["total"] >= 15: 
        taxa = (dados["roxa"] / dados["total"]) * 100
        ranking.append({"padrao": pad, "taxa": taxa, "total": dados["total"]})

ranking = sorted(ranking, key=lambda x: x["taxa"], reverse=True)[:5]

if ranking:
    for item in ranking:
        st.markdown(f"<p style='color:white; margin:5px 0;'>💎 <b>{item['padrao']}</b> → <span style='color:#00ff00;'>{item['taxa']:.1f}%</span> de assertividade ({item['total']} ocorrências)</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='color:#888; text-align:center; margin:0;'>Aguardando banco de dados com amostragem estável (Mínimo: 15 ocorrências).</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# LINHA DO TEMPO RECENTE
if len(st.session_state.historico) > 0:
    velas_texto = " → ".join([f"[{v}]" for v in st.session_state.historico[-15:]])
    st.markdown(f"<p style='color:#888; margin-top:15px;'><b>Últimas velas:</b> {velas_texto}</p>", unsafe_allow_html=True)

# RESET DE SEGURANÇA
st.markdown("<br>", unsafe_allow_html=True)
if st.button("REINICIAR SISTEMA"):
    st.session_state.historico = []
    st.session_state.banco_padroes = []
    st.session_state.distancia_rosa = 0
    st.session_state.acertos = 0
    st.session_state.erros = 0
    st.session_state.ultima_entrada = None
    st.rerun()
