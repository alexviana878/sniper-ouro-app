import streamlit as st
from datetime import datetime
from collections import defaultdict

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
# 📂 TREINAMENTO VIA CSV COM ENGINE DE PESO TEMPORAL
# =========================================================
st.markdown('<div class="main-card">### 📂 TREINAR INTELIGÊNCIA</div>', unsafe_allow_html=True)
arquivo = st.file_uploader("Envie CSV/TXT com 1 vela por linha:", type=["csv", "txt"])

if arquivo is not None and len(st.session_state.historico) == 0:
    linhas = arquivo.read().decode("utf-8").splitlines()
    velas_carga = []
    for linha in linhas:
        try:
            limpo = linha.strip()
            if not limpo: continue
            velas_carga.append(float(limpo.replace(",", ".")))
        except: pass
        
    total_velas = len(velas_carga)
    
    # Injeção Inteligente com Peso Temporal
    for idx, valor in enumerate(velas_carga):
        distancia_do_fim = total_velas - idx
        
        if distancia_do_fim <= 300: peso = 5       
        elif distancia_do_fim <= 1000: peso = 3    
        else: peso = 1                             
        
        if len(st.session_state.historico) >= 5:
            padrao_existente = gerar_padrao(st.session_state.historico)
            for _ in range(peso):
                salvar_padrao(padrao_existente, valor)
                
        st.session_state.historico.append(valor)
        st.session_state.distancia_rosa = 0 if valor >= 10.0 else st.session_state.distancia_rosa + 1

    st.success(f"🔥 {total_velas} velas integradas e calibradas com matriz de peso.")

# =========================================================
# ANALISADOR DE PADRÕES (UPGRADE DEFAULTDICT)
# =========================================================
def analisar_padroes():
    memoria = defaultdict(lambda: {"total": 0, "roxa": 0
