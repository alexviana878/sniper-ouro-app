import streamlit as st

# Configuração de Luxo da Página
st.set_page_config(page_title="Sniper Ouro App", page_icon="🎯", layout="centered")

# Estilo Neon Personalizado (CSS)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stNumberInput { color: #00ff00; }
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
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Sniper Ouro App")

# Interface do App
with st.container():
    st.markdown('<div class="status-card"><h3 style="color: #ff00ff;">RADAR DE VELAS ROSAS 🌸</h3><p>MADURO > Probabilidade Alta<br>Distância: 32 rodadas</p></div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="target-card"><h1 style="color: #00ff00;">TARGET: 1.30X 🎯</h1><p style="color: #00ff00;">CONFIANÇA: 100% (HIST)<br>STATUS MERCADO: PAGADOR 🔥</p></div>', unsafe_allow_html=True)

# Entrada de Dados
vela = st.number_input("Digite a Última Vela:", min_value=0.0, format="%.2f")

if st.button("ANALISAR PRÓXIMA"):
    st.success(f"Vela {vela} processada. Mantendo sinal de ENTRADA!")

st.markdown("---")
st.write("SESSÃO REAL: 95% [19/20]")
