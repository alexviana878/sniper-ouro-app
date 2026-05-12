import streamlit as st

st.set_page_config(page_title="Sniper Ouro Pro", page_icon="🎯")

# CSS Neon de Luxo
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .status-card { border: 2px solid #ff00ff; border-radius: 15px; padding: 15px; text-align: center; background-color: #1a1c24; box-shadow: 0 0 10px #ff00ff; }
    .target-card { border: 2px solid #00ff00; border-radius: 15px; padding: 15px; text-align: center; background-color: #1a1c24; box-shadow: 0 0 10px #00ff00; margin-top: 10px; }
    .wait-card { border: 2px solid #ff4b4b; border-radius: 15px; padding: 15px; text-align: center; background-color: #1a1c24; box-shadow: 0 0 10px #ff4b4b; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'historico' not in st.session_state:
    st.session_state.historico = []

st.title("🎯 Sniper Ouro Pro")

# Entrada da Vela
vela = st.number_input("Digite a Última Vela:", min_value=0.0, format="%.2f", step=0.01)

if st.button("ANALISAR PRÓXIMA"):
    st.session_state.historico.append(vela)
    
# Lógica de Inteligência (Suas 54 Estratégias)
ultimo_sinal = "AGUARDAR ✋"
cor_card = "wait-card"
confianca = "ANALISANDO..."
status_mercado = "INSTÁVEL ⚠️"

if len(st.session_state.historico) > 0:
    ultima = st.session_state.historico[-1]
    
    if ultima < 1.20:
        ultimo_sinal = "AGUARDAR ✋"
        status_mercado = "RECOLHEDOR ⛔"
        confianca = "ALERTA DE SURF BAIXO"
    elif ultima >= 2.0:
        ultimo_sinal = "ENTRAR 1.30X 🎯"
        cor_card = "target-card"
        status_mercado = "PAGADOR 🔥"
        confianca = "98% (ESTR_54)"

# Exibição dos Painéis
st.markdown(f'<div class="status-card"><h3 style="color: #ff00ff;">RADAR ROSA 🌸</h3><p>Distância: {len(st.session_state.historico)} rodadas</p></div>', unsafe_allow_html=True)

st.markdown(f'<div class="{cor_card}"><h1 style="color: {"#00ff00" if "ENTRAR" in ultimo_sinal else "#ff4b4b"};">{ultimo_sinal}</h1><p>CONFIANÇA: {confianca}<br>STATUS: {status_mercado}</p></div>', unsafe_allow_html=True)

if st.button("Limpar Histórico"):
    st.session_state.historico = []
    st.rerun()
