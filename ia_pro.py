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
# CSS PREMIUM RE-ESTILIZADO (PAINEL SEGURO)
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
# BANCO DE DADOS LOCAL E ARMAZENAMENTO EM CACHE
# =========================================================
ARQUIVO_BANCO = "memoria_extrema.txt"

def salvar_vela_no_disco(valor):
    with open(ARQUIVO_BANCO, "a") as f:
        f.write(f"{valor}\n")

@st.cache_data(show_spinner=False)
def carregar_banco_do_disco_cached(mod_time):
    if not os.path.exists(ARQUIVO_BANCO):
        return []
    velas = []
    with open(ARQUIVO_BANCO, "r") as f:
        for linha in f:
            try:
                velas.append(float(linha.strip()))
            except: pass
    return velas

def obter_velas_vivas():
    mtime = os.path.getmtime(ARQUIVO_BANCO) if os.path.exists(ARQUIVO_BANCO) else 0
    return carregar_banco_do_disco_cached(mtime)

# =========================================================
# INICIALIZAÇÃO DE VARIÁVEIS DE SESSÃO
# =========================================================
if "historico" not in st.session_state:
    st.session_state.historico = obter_velas_vivas()

if "banco_padroes" not in st.session_state: st.session_state.banco_padroes = []
if "distancia_rosa" not in st.session_state: st.session_state.distancia_rosa = 0
if "acertos" not in st.session_state: st.session_state.acertos = 0
if "erros" not in st.session_state: st.session_state.erros = 0
if "ultima_entrada" not in st.session_state: st.session_state.ultima_entrada = None

# RELÓGIO OPERACIONAL
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
    <p style='color:#f59e0b !important; font-weight:bold; font-size:16px; margin-top:0;'>🛡️ O SEGREDO NÃO É PREVER TUDO, É ELIMINAR O RISCO RUIM</p>
    <table style='width:100%; border-collapse: collapse; margin-top:10px;'>
        <tr><th>NÍVEL DO SISTEMA</th><th>ASSERTIVIDADE REAL ESPERADA</th></tr>
        <tr><td>🔵 <b>Profissional Quant</b></td><td><b>70% a 80% (Filtros de Defesa Ativos)</b></td></tr>
    </table>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# OPERAÇÕES DE CLASSIFICAÇÃO MATEMÁTICA
# =========================================================
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

# Nome alterado para evitar problemas com tradutores automáticos
def registrar_padrao_no_banco(padrao, resultado):
    st.session_state.banco_padroes.append({"padrao": padrao, "resultado": resultado})

@st.cache_data(show_spinner=False)
def treinar_matriz_cached(velas_input):
    banco_retorno = []
    total_velas = len(velas_input)
    if total_velas >= 5:
        historico_temporario = []
        for idx, valor in enumerate(velas_input):
            distancia_do_fim = total_velas - idx
            if distancia_do_fim <= 200: peso = 4       
            elif distancia_do_fim <= 800: peso = 2    
            else: peso = 1                             
            
            if len(historico_temporario) >= 4:
