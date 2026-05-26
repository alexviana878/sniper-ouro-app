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
# MASTER LOGIN RESTRITO
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
.manifesto-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 15px; margin-bottom: 15px; }
th, td { padding: 8px; text-align: left; border-bottom: 1px solid #30363d; color: white; }
th { background-color: #21262d; color: #f59e0b; }
h1,h2,h3,p,label { color: white !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# BANCO DE DADOS LOCAL (MEMÓRIA PERMANENTE NO SERVIDOR)
# =========================================================
ARQUIVO_BANCO = "memoria_extrema.txt"

def salvar_vela_no_disco(valor):
    with open(ARQUIVO_BANCO, "a") as f:
        f.write(f"{valor}\n")

def carregar_banco_do_disco():
    if not os.path.exists(ARQUIVO_BANCO):
        return []
    velas = []
    with open(ARQUIVO_BANCO, "r") as f:
        for linha in f:
            try:
                velas.append(float(linha.strip()))
            except: pass
    return velas

# =========================================================
# INICIALIZAÇÃO DE VARIÁVEIS DE SESSÃO
# =========================================================
if "historico" not in st.session_state:
    st.session_state.historico = carregar_banco_do_disco()

if "banco_padroes" not in st.session_state: st.session_state.banco_padroes = []
if "distancia_rosa" not in st.session_state: st.session_state.distancia_rosa = 0
if "acertos" not in st.session_state: st.session_state.acertos = 0
if "erros" not in st.session_state: st.session_state.erros = 0
if "ultima_entrada" not in st.session_state: st.session_state.ultima_entrada = None

# =========================================================
# RELÓGIO DE JANELAS DE TEMPO
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
# 🧠 MANIFESTO DA MENTALIDADE INSTITUCIONAL
# =========================================================
with st.expander("🧠 DIRETRIZES DA MENTALIDADE SNIPER ELITE"):
    st.markdown("""
    <div class="manifesto-card">
    <p style='color:#f59e0b !important; font-weight:bold; font-size:16px; margin-top:0;'>🛡️ O SEGREDO NÃO É PREVER TUDO, É ELIMINAR O RISCO RUIM</p>
    <p style='font-size:14px; color:#c9d1d9;'>O algoritmo do mercado muda de intensidade e frequência. Sistemas profissionais trabalham com <b>Vantagem Matemática Contextual</b>, operando pouco e recusando sinais medianos.</p>
    <table style='width:100%; border-collapse: collapse; margin-top:10px;'>
        <tr><th>NÍVEL DO SISTEMA</th><th>ASSERTIVIDADE REAL ESPERADA</th></tr>
        <tr><td>🔴 Amador / Fake</td><td>35% a 50% (Gera ruído aleatório)</td></tr>
        <tr><td>🟡 Médio Comercial</td><td>50% a 60% (Entra sem contexto)</td></tr>
        <tr><td>🟢 Bom de Mercado</td><td>60% a 70% (Histórico simples)</td></tr>
        <tr><td>🔵 <b>Profissional Quant</b></td><td><b>70% a 80% (Filtros de Defesa Ativos)</b></td></tr>
        <tr><td>👑 Sniper Elite</td><td>80%+ (Apenas em Confluências Raras)</td></tr>
    </table>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# CLASSIFICAÇÃO INTELIGENTE DE 6 CAMADAS
# =========================================================
def classificar_vela(valor):
    if valor < 1.20: return "X"    
    elif valor < 2.00: return "B"  
    elif valor < 5.00: return "R"  
    elif valor < 10.00: return "P" 
    elif valor < 20.00: return "A" 
    else: return "E"               

# 🎯 UPGRADE EXTREMO: REDUÇÃO DA JANELA DE PADRÃO DE 5 PARA 4 ELEMENTOS
def gerar_padrao(historico):
    if len(historico) < 4: return None
    return "-".join([classificar_vela(v) for v in historico[-4:]])

def salvar_padrao(padrao, resultado):
    st.session_state.banco_padroes.append({"padrao": padrao, "resultado": resultado})

# MODULO DE RE-TREINAMENTO OPERACIONAL (4 VELAS)
def treinar_matriz_completa():
    st.session_state.banco_padroes = []
    total_velas = len(st.session_state.historico)
    if total_velas >= 5:
        historico_temporario = []
        for idx, valor in enumerate(st.session_state.historico):
            distancia_do_fim = total_velas - idx
            if distancia_do_fim <= 200: peso = 4       
            elif distancia_do_fim <= 800: peso = 2    
            else: peso = 1                             
            
            if len(historico_temporario) >= 4:
                padrao_existente = gerar_padrao(historico_temporario)
                if padrao_existente:
                    for _ in range(peso):
                        salvar_padrao(padrao_existente, valor)
            historico_temporario.append(valor)

if len(st.session_state.historico) > 0 and len(st.session_state.banco_padroes) == 0:
    treinar_matriz_completa()

# =========================================================
# 📂 REPOSITÓRIO DE CARGA CSV 
# =========================================================
st.markdown('<div class="main-card">### 📂 TREINAR INTELIGÊNCIA EXTREMA</div>', unsafe_allow_html=True)
arquivo = st.file_uploader("Suba um novo histórico CSV para expandir o cérebro da IA:", type=["csv", "txt"])

if arquivo is not None:
    linhas = arquivo.read().decode("utf-8").splitlines()
    contador_carga = 0
    for linha in linhas:
        try:
            limpo = linha.strip().replace('"', '').replace("'", "")
            if not limpo: continue
            partes = limpo.split()
            for parte in partes:
                val_limpo = parte.replace(",", ".")
                v_num = float(val_limpo)
                salvar_vela_no_disco(v_num)
                contador_carga += 1
                break
        except: pass
    if contador_carga > 0:
        st.session_state.historico = carregar_banco_do_disco()
        treinar_matriz_completa()
        st.success(f"🔥 Banco permanente expandido com +{contador_carga} velas com sucesso!")
        st.rerun()

# =========================================================
# ANALISADOR DE PADRÕES 
# =========================================================
def analisar_padroes():
    memoria = {}
    if not st.session_state.banco_padroes: return memoria
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
# SCORE EXTREMO CALIBRADO NO PONTO IDEAL
# =========================================================
def calcular_score(historico, taxa_roxa, taxa_rosa, ocorrencias):
    score = 0
    if len(historico) < 4: return 0

    v_atual = historico[-1]
    ultimas5 = historico[-5:] if len(historico) >= 5 else historico

    azuis = sum(1 for x in ultimas5 if x < 2.0)
    extremos = sum(1 for x in ultimas5 if x < 1.20)

    if azuis >= 4: score -= 10
    if extremos >= 2: score -= 8
    if v_atual < 1.10: score -= 10

    if taxa_roxa >= 70: score += 5
    if taxa_roxa >= 80: score += 3
    if taxa_roxa >= 90: score += 4
    if taxa_rosa >= 15: score += 3
    
    # Pesos de amostragem ajustados para o Ponto Ideal
    if ocorrencias >= 3: score += 3
    if ocorrencias >= 10: score += 4
    if ocorrencias >= 25: score += 4
    
    if janela_ativa: score += 2
    if st.session_state.distancia_rosa >= 10: score += 2
    if len(historico) >= 2 and historico[-2] >= 2.0: score += 2
    return score

# =========================================================
# PROCESSAMENTO CENTRAL EXTREMO
# =========================================================
def processar_sinal(historico):
    if len(historico) < 20:
        return "ANALISANDO...", "red-card",
