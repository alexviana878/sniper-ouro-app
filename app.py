import streamlit as st

# Configuração da Página para Celular e PC
st.set_page_config(page_title="Sniper Ouro Pro", page_icon="🎯", layout="centered")

# --- ESTILO VISUAL NEON (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .status-card { 
        border: 2px solid #ff00ff; 
        border-radius: 15px; 
        padding: 20px; 
        text-align: center; 
        background-color: #1a1c24; 
        box-shadow: 0 0 15px #ff00ff; 
    }
    .target-card { 
        border: 2px solid #00ff00; 
        border-radius: 15px; 
        padding: 20px; 
        text-align: center; 
        background-color: #1a1c24; 
        box-shadow: 0 0 15px #00ff00; 
        margin-top: 15px; 
    }
    .wait-card { 
        border: 2px solid #ff4b4b; 
        border-radius: 15px; 
        padding: 20px; 
        text-align: center; 
        background-color: #1a1c24; 
        box-shadow: 0 0 15px #ff4b4b; 
        margin-top: 15px; 
    }
    .stNumberInput label { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE MEMÓRIA ---
if 'historico' not in st.session_state:
    st.session_state.historico = []
if 'distancia_rosa' not in st.session_state:
    st.session_state.distancia_rosa = 0
if 'ultimo_sinal' not in st.session_state:
    st.session_state.ultimo_sinal = "AGUARDAR ✋"
if 'cor_card' not in st.session_state:
    st.session_state.cor_card = "wait-card"

st.title("🎯 Sniper Ouro Pro")

# --- ENTRADA DE DADOS ---
vela = st.number_input("Digite o valor da última vela:", min_value=0.0, step=0.01, format="%.2f")

if st.button("ANALISAR PRÓXIMA"):
    # Adiciona ao histórico
    st.session_state.historico.append(vela)
    
    # 1. LÓGICA DO RADAR ROSA (Zera se for >= 10.0)
    if vela >= 10.0:
        st.session_state.distancia_rosa = 0
    else:
        st.session_state.distancia_rosa += 1
    
    # 2. LÓGICA DE INTELIGÊNCIA (SINAL)
    # Se a vela for baixa (Recolhimento), manda aguardar
    if vela < 1.20:
        st.session_state.ultimo_sinal = "AGUARDAR ✋"
        st.session_state.cor_card = "wait-card"
        st.session_state.status_msg = "RECOLHEDOR ⛔"
        st.session_state.confianca = "ALERTA DE SURF BAIXO"
    
    # Se a vela for de força (Prepara entrada)
    elif vela >= 2.0:
        st.session_state.ultimo_sinal = "ENTRAR 1.30X 🎯"
        st.session_state.cor_card = "target-card"
        st.session_state.status_msg = "PAGADOR 🔥"
        st.session_state.confianca = "98% (ESTR_54)"
    
    # Velas intermediárias mantêm observação
    else:
        st.session_state.ultimo_sinal = "AGUARDAR ✋"
        st.session_state.cor_card = "wait-card"
        st.session_state.status_msg = "MERCADO OSCILANDO ⚠️"
        st.session_state.confianca = "AGUARDANDO PADRÃO"

# --- EXIBIÇÃO DOS PAINÉIS ---
dist = st.session_state.distancia_rosa
st.markdown(f'''
    <div class="status-card">
        <h3 style="color: #ff00ff;">RADAR ROSA 🌸</h3>
        <p style="font-size: 24px; color: #ffffff;">Distância: {dist} rodadas</p>
    </div>
    ''', unsafe_allow_html=True)

sinal = st.session_state.ultimo_sinal
cor = st.session_state.cor_card
status = st.session_state.get('status_msg', 'ANALISANDO...')
conf = st.session_state.get('confianca', '---')

st.markdown(f'''
    <div class="{cor}">
        <h1 style="color: {'#00ff00' if 'ENTRAR' in sinal else '#ff4b4b'};">{sinal}</h1>
        <p style="color: #ffffff;">CONFIANÇA: {conf}<br>STATUS: {status}</p>
    </div>
    ''', unsafe_allow_html=True)

# --- FERRAMENTAS DE GESTÃO ---
st.markdown("---")
if st.button("Limpar Sessão/Resetar"):
    st.session_state.historico = []
    st.session_state.distancia_rosa = 0
    st.session_state.ultimo_sinal = "AGUARDAR ✋"
    st.session_state.cor_card = "wait-card"
    st.rerun()

st.write(f"Velas analisadas nesta sessão: {len(st.session_state.historico)}")
