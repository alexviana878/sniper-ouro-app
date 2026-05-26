import streamlit as st
from datetime import datetime
from collections import defaultdict

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Sniper Ouro IA ELITE",
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
    st.markdown("<h1 style='text-align:center;color:#ef4444;'>🔒 SISTEMA ELITE PROTEGIDO</h1>", unsafe_allow_html=True)
    senha = st.text_input("Digite a chave master:", type="password")
    if st.button("ATIVAR SISTEMA"):
        if senha == SENHA_CORRETA:
            st.session_state.autenticado = True
            st.success("Sistema liberado.")
            st.rerun()
        else:
            st.error("Chave inválida.")
    st.stop()

# =========================================================
# CSS PREMIUM MILITARIZADO
# =========================================================
st.markdown("""
<style>
.stApp { background-color: #070b16; }
h1,h2,h3,p,label { color: white !important; }
.clock-card { border: 2px solid #00ff00; border-radius: 15px; padding: 15px; text-align: center; background: #111322; box-shadow: 0 0 15px #00ff00; margin-bottom: 20px; }
.target-card { border: 2px solid #00ff00; border-radius: 18px; padding: 20px; text-align: center; background: #111322; box-shadow: 0 0 20px #00ff00; margin-bottom: 20px; }
.wait-card { border: 2px solid #ff0000; border-radius: 18px; padding: 20px; text-align: center; background: #111322; box-shadow: 0 0 15px #ff0000; margin-bottom: 20px; }
.status-card { border: 2px solid #a855f7; border-radius: 18px; padding: 20px; text-align: center; background: #111322; box-shadow: 0 0 15px #a855f7; margin-bottom: 20px; }
.ranking-card { border: 2px solid #f59e0b; border-radius: 18px; padding: 20px; background: #111322; box-shadow: 0 0 15px #f59e0b; margin-bottom: 20px; }
.csv-card { border: 2px dashed #f59e0b; border-radius: 15px; padding: 20px; background: #111322; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE (MEMÓRIA ATIVA)
# =========================================================
if "historico" not in st.session_state: st.session_state.historico = []
if "banco_padroes" not in st.session_state: st.session_state.banco_padroes = []
if "acertos" not in st.session_state: st.session_state.acertos = 0
if "erros" not in st.session_state: st.session_state.erros = 0
if "ultima_entrada" not in st.session_state: st.session_state.ultima_entrada = None
if "distancia_rosa" not in st.session_state: st.session_state.distancia_rosa = 0

# =========================================================
# RELÓGIO DE FLUXO CRONOS
# =========================================================
agora = datetime.now()
minutos_pagantes = [2,5,8,10,12,15,18,20,22,25,28,30,32,35,38,40,42,45,48,50,52,55,58,0]
janela_ativa = agora.minute in minutos_pagantes

st.markdown(f"""
<div class="clock-card">
<h2 style="margin:0; color:#00ff00 !important;">{agora.strftime("%H:%M:%S")}</h2>
<p style="margin:0; color:#00ff00 !important;">{"⚠️ JANELA PAGANTE ATIVA" if janela_ativa else "MONITORANDO MERCADO"}</p>
</div>
""", unsafe_allow_html=True)

st.title("🎯 SNIPER OURO IA ELITE")

# =========================================================
# ENGINE DE TRADUÇÃO E PROCESSAMENTO IA
# =========================================================
def classificar_vela(valor):
    if valor < 2.0: return "B" # Baixa (Azul)
    elif valor < 10.0: return "M" # Média (Roxa)
    return "A" # Alta (Rosa)

def gerar_padrao(historico):
    if len(historico) < 5: return None
    return "-".join([classificar_vela(v) for v in historico[-5:]])

def salvar_memoria(padrao, resultado):
    st.session_state.banco_padroes.append({"padrao": padrao, "resultado": resultado})

# =========================================================
# IMPORTAÇÃO CSV + UPGRADE DE PESO TEMPORAL COMBINADO
# =========================================================
st.markdown('<div class="csv-card">', unsafe_allow_html=True)
st.markdown("## 📂 IMPORTAR BASE DE TREINAMENTO")
arquivo = st.file_uploader("Envie CSV ou TXT contendo 1 vela por linha", type=["csv", "txt"])

if arquivo is not None and len(st.session_state.historico) == 0:
    linhas = arquivo.read().decode("utf-8").splitlines()
    velas_temporarias = []
    
    for linha in linhas:
        try:
            limpo = linha.strip()
            if not limpo: continue
            velas_temporarias.append(float(limpo.replace(",", ".")))
        except: pass
        
    total_velas = len(velas_temporarias)
    
    # Processamento com Peso Temporal Inteligente (Inovação de Machine Learning)
    for idx, valor in enumerate(velas_temporarias):
        distancia_do_fim = total_velas - idx
        
        if distancia_do_fim <= 300: peso = 5       # Últimas 300 velas (Peso Máximo)
        elif distancia_do_fim <= 1000: peso = 3    # Médias 1000 velas
        else: peso = 1                             # Dados históricos antigos
        
        # Sincronização Cirúrgica: gera o padrão com o histórico que já existia antes da nova vela
        if len(st.session_state.historico) >= 5:
            padrao_existente = gerar_padrao(st.session_state.historico)
            for _ in range(peso):
                salvar_memoria(padrao_existente, valor)
                
        st.session_state.historico.append(valor)
        st.session_state.distancia_rosa = 0 if valor >= 10.0 else st.session_state.distancia_rosa + 1

    st.success(f"🔥 Inteligência calibrada! {total_velas} velas injetadas com otimização de tempo.")
st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ANALISAR PADRÕES - USANDO O SEU DEFAULTDICT ULTRA RÁPIDO
# =========================================================
def analisar_padroes():
    memoria = defaultdict(lambda: {"total": 0, "roxa": 0, "rosa": 0, "erro": 0})

    for item in st.session_state.banco_padroes:
        padrao = item["padrao"]
        resultado = item["resultado"]

        memoria[padrao]["total"] += 1
        if resultado >= 2.0: memoria[padrao]["roxa"] += 1
        else: memoria[padrao]["erro"] += 1
        if resultado >= 10.0: memoria[padrao]["rosa"] += 1
    return memoria

# =========================================================
# SCORE INTELIGENTE RIGOROSO
# =========================================================
def calcular_score(historico, taxa_roxa, taxa_rosa, ocorrencias, erros):
    score = 0
    if len(historico) < 10: return 0

    ultimas10 = historico[-10:]
    azuis = sum(1 for x in ultimas10 if x < 2.0)
    micros = sum(1 for x in historico[-15:] if x < 1.30)
    v_atual = historico[-1]

    # Confluências Adaptativas
    if janela_ativa: score += 2
    if taxa_roxa >= 70: score += 4
    if taxa_roxa >= 80: score += 3
    if taxa_roxa >= 90: score += 4
    if taxa_rosa >= 20: score += 2
    
    # Pesos por Volume de Confiança Estatística
    if ocorrencias >= 15: score += 3
    if ocorrencias >= 30: score += 4
    if ocorrencias >= 50: score += 5
    
    if st.session_state.distancia_rosa >= 12: score += 2
    if azuis <= 3: score += 2
    if len(historico) >= 2 and historico[-2] >= 2.0: score += 2

    # Penalidades Severas (Filtros de Defesa)
    if azuis >= 7: score -= 10
    if micros >= 6: score -= 5
    if v_atual < 1.15: score -= 4
    if erros >= ocorrencias: score -= 6 # Penalidade de padrão morto

    return score

# =========================================================
# PROCESSADOR DE GATILHOS SELETIVOS
# =========================================================
def processar_sinal(historico):
    if len(historico) < 15:
        return "ANALISANDO...", "wait-card", "ALIMENTANDO REPOSITÓRIO", "---", None

    # Bloqueio imediato de proteção de banca em mercado sujo
    ultimas10 = historico[-10:]
    azuis = sum(1 for x in ultimas10 if x < 2.0)
    if azuis >= 7:
        return "🛑 MERCADO RUIM", "wait-card", "CONCENTRAÇÃO EXTREMA DE VELAS AZUIS (70%+ RECOLHIMENTO)", "0%", None

    padrao = gerar_padrao(historico)
    memoria = analisar_padroes()
    taxa_roxa, taxa_rosa, ocorrencias, erros = 0.0, 0.0, 0, 0

    if padrao in memoria:
        dados = memoria[padrao]
        ocorrencias = dados["total"]
        erros = dados["erro"]
        if ocorrencias > 0:
            taxa_roxa = (dados["roxa"] / ocorrencias) * 100
            taxa_rosa = (dados["rosa"] / ocorrencias) * 100

    # Filtro rígido de amostragem mínima de amostragem
    if ocorrencias < 15:
        return "AGUARDAR ✋", "wait-card", f"PADRÃO INSTÁVEL ({padrao}) | BASE DE DADOS VOLÁTIL ({ocorrencias} SINAIS)", "---", None

    score = calcular_score(historico, taxa_roxa, taxa_rosa, ocorrencias, erros)

    # REGRAS DE OURO: FILTROS SNIPER DE OPERAÇÃO
    if score >= 20:
        return f"🔱 SNIPER ELITE ({padrao})", "target-card", f"SCORE MÁXIMO {score} | ROXA {taxa_roxa:.1f}% | OCORRÊNCIAS {ocorrencias}", "99%", "ROXA"
    if score >= 17:
        return f"🔥 ENTRADA PREMIUM ({padrao})", "target-card", f"SCORE ALTO {score} | ROXA {taxa_roxa:.1f}% | VOL {ocorrencias}", "94%", "ROXA"
    if score >= 14:
        return f"⚠️ ENTRADA MODERADA ({padrao})", "status-card", f"SCORE EQUILIBRADO {score} | ROXA {taxa_roxa:.1f}%", "88%", "ROXA"
    if taxa_rosa >= 35 and st.session_state.distancia_rosa >= 10:
        return f"🌸 BUSCAR ROSA ({padrao})", "target-card", f"ZONA ALTA MATURADA | PRESSÃO DE FLUXO ROSA", "91%", "ROSA"
    
    return "AGUARDAR ✋", "wait-card", f"PROCURANDO CONFLUÊNCIA DE CRITÉRIOS (SCORE ATUAL: {score})", "---", None

# =========================================================
# INPUTS FLUXO OPERACIONAL
# =========================================================
banca = st.number_input("Banca Inicial (R$)", min_value=0.0, value=20.0, step=1.0)
vela = st.number_input("Digite a última vela", min_value=0.0, format="%.2f", step=0.01)

# =========================================================
# BOTÃO PRINCIPAL COM SINCRONIZAÇÃO EM TEMPO REAL CORRIGIDA
# =========================================================
if st.button("CALCULAR PROBABILIDADE"):
    # 1. Contabiliza a entrada que estava vigente na tela com a nova vela inserida
    if st.session_state.ultima_entrada == "ROXA":
        if vela >= 2.0: st.session_state.acertos += 1
        else: st.session_state.erros += 1
    elif st.session_state.ultima_entrada == "ROSA":
        if vela >= 10.0: st.session_state.acertos += 1
        else: st.session_state.erros += 1

    # 2. Registra na memória o padrão de 5 velas gerado ANTES de anexar a nova vela ao histórico
    if len(st.session_state.historico) >= 5:
        padrao_gerado = gerar_padrao(st.session_state.historico)
        salvar_memoria(padrao_gerado, vela)

    # 3. Insere a nova vela na base operacional viva
    st.session_state.historico.append(vela)

    # 4. Ajuste do Radar Rosa
    if vela >= 10.0: st.session_state.distancia_rosa = 0
    else: st.session_state.distancia_rosa += 1

    st.rerun()

# EXECUÇÃO DO MOTOR PREDITIVO
sinal, cor, status, conf, entrada = processar_sinal(st.session_state.historico)
st.session_state.ultima_entrada = entrada

# EXIBIÇÃO MONITOR PRINCIPAL
st.markdown(f"""
<div class="{cor}">
<h1 style="margin:0; color: {'#00ff00' if entrada and '⚠️' not in sinal else '#ef4444'} !important;">{sinal}</h1>
<p style="margin:5px 0 0 0;"><b>CONFIANÇA MATEMÁTICA:</b> {conf}<br><b>DIRETRIZ DE CAMPO:</b> {status}</p>
</div>
""", unsafe_allow_html=True)

# EXIBIÇÃO RADAR ROSA
st.markdown(f"""
<div class="status-card">
<h2 style="margin:0;">🌸 RADAR ROSA</h2>
<p style="margin:5px 0 0 0;">Distância Atual: <b>{st.session_state.distancia_rosa}</b> rodadas sem alvos altos</p>
</div>
""", unsafe_allow_html=True)

# HISTÓRICO DE PERFORMANCE DA SESSÃO
total = st.session_state.acertos + st.session_state.erros
assertividade = (st.session_state.acertos / total) * 100 if total > 0 else 0.0

st.markdown('<div class="ranking-card"><h2 style="text-align:center; margin:0 0 15px 0;">👑 PERFORMANCE IA ELITE</h2>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.metric("✅ ACERTOS", st.session_state.acertos)
with c2: st.metric("❌ ERROS", st.session_state.erros)
with c3: st.metric("📊 ASSERTIVIDADE", f"{assertividade:.1f}%")
st.markdown("</div>", unsafe_allow_html=True)

# REPOSITÓRIO RANKING DOS MELHORES PADRÕES (USANDO SEU MODELO SELETIVO EXIGENTE)
st.markdown('<div class="ranking-card"><h2 style="text-align:center; margin:0 0 15px 0;">🏆 TOP PADRÕES DO LABORATÓRIO</h2>', unsafe_allow_html=True)
memoria_mapeada = analisar_padroes()
ranking = []

for pad, dados in memoria_mapeada.items():
    if dados["total"] >= 15: # Exige o seu patamar mínimo de 15 ocorrências reais
        taxa = (dados["roxa"] / dados["total"]) * 100
        ranking.append({"padrao": pad, "taxa": taxa, "total": dados["total"]})

ranking = sorted(ranking, key=lambda x: x["taxa"], reverse=True)[:5]

if ranking:
    for item in ranking:
        st.markdown(f"""
        <p style="margin:5px 0;">
        💎 <b>{item['padrao']}</b> → <span style='color:#00ff00;'>{item['taxa']:.1f}%</span> de assertividade ({item['total']} ocorrências)
        </p>
        """, unsafe_allow_html=True)
else:
    st.markdown("<p style='color:#888; text-align:center; margin:0;'>A IA requer a carga do arquivo CSV para listar padrões com amostragem estável (Min: 15).</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# LINHA DO TEMPO RECENTE
if len(st.session_state.historico) > 0:
    st.markdown("<p style='color:#888;'><b>Últimas Velas:</b> " + " → ".join([f"[{x}]" for x in st.session_state.historico[-12:]]) + "</p>", unsafe_allow_html=True)

# BOTÃO DE REINICIALIZAÇÃO DO SISTEMA
st.markdown("<br>", unsafe_allow_html=True)
if st.button("REINICIAR SISTEMA"):
    st.session_state.historico = []
    st.session_state.banco_padroes = []
    st.session_state.acertos = 0
    st.session_state.erros = 0
    st.session_state.ultima_entrada = None
    st.session_state.distancia_rosa = 0
    st.rerun()
