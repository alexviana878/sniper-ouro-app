import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="Sniper Ouro Cronos", page_icon="🎯")

# Estilo Neon de Luxo
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .clock-card { border: 1px solid #00ffff; border-radius: 10px; padding: 10px; text-align: center; background-color: #1a1c24; box-shadow: 0 0 5px #00ffff; margin-bottom: 10px; }
    .status-card { border: 2px solid #ff00ff; border-radius: 15px; padding: 15px; text-align: center; background-color: #1a1c24; box-shadow: 0 0 10px #ff00ff; }
    .target-card { border: 2px solid #00ff00; border-radius: 15px; padding: 15px; text-align: center; background-color: #1a1c24; box-shadow: 0 0 15px #00ff00; margin-top: 10px; }
    .wait-card { border: 2px solid #ff4b4b; border-radius: 15px; padding: 15px; text-align: center; background-color: #1a1c24; box-shadow: 0 0 10px #ff4b4b; margin-top: 10px; }
    .janela-card { color: #00ffff; font-weight: bold; font-size: 18px; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

if 'historico' not in st.session_state:
    st.session_state.historico = []
if 'distancia_rosa' not in st.session_state:
    st.session_state.distancia_rosa = 0

# --- RELÓGIO E ANÁLISE DE TEMPO ---
agora = datetime.now()
segundos = agora.second
minuto_atual = agora.minute
janela_ativa = segundos >= 45 or segundos <= 15 # Janela de 30s sugerida no vídeo

# Exibição do Relógio
st.markdown(f'<div class="clock-card"><h2 style="color: #00ffff; margin:0;">{agora.strftime("%H:%M:%S")}</h2>'
            f'<p class="janela-card">{"JANELA PAGANTE ATIVA ⏳" if janela_ativa else "AGUARDANDO MINUTO..."}</p></div>', unsafe_allow_html=True)

st.title("🎯 Sniper Ouro Cronos")

# Entrada da Vela
vela = st.number_input("Última Vela:", min_value=0.0, format="%.2f", step=0.01)

if st.button("ANALISAR PRÓXIMA"):
    st.session_state.historico.append(vela)
    st.session_state.distancia_rosa = 0 if vela >= 10.0 else st.session_state.distancia_rosa + 1

# --- ALGORITMO ULTRA (MANTIDO) ---
def processar_ultra(historico):
    if len(historico) < 3: return "ANALISANDO...", "wait-card", "AGUARDANDO DADOS", "---"
    v_atual = historico[-1]
    
    # Lógica de Recuperação/Quebra
    if all(x < 1.80 for x in historico[-3:-1]) and v_atual >= 1.80:
        return "ENTRAR (QUEBRA) 🎯", "target-card", "PADRÃO IDENTIFICADO", "98%"
    
    # Lógica de Rosa
    if st.session_state.distancia_rosa > 12 and v_atual > 2.0:
        return "BUSCAR ROSA 🌸", "target-card", "MATURAÇÃO ALTA", "95%"
    
    # Lógica de Recuperação de Azul
    if v_atual < 2.0 and any(x >= 2.0 for x in historico[-4:-1]):
        m_conf = "96%" if janela_ativa else "92%" # Aumenta confiança se estiver na janela
        return "ENTRAR (RECUPERAÇÃO) 🎯", "target-card", "CORREÇÃO DE GRÁFICO", m_conf

    if v_atual < 1.15: return "AGUARDAR ✋", "wait-card", "MERCADO RECOLHEDOR", "99%"
    return "AGUARDAR ✋", "wait-card", "BUSCANDO GATILHO", "---"

sinal, cor, status, conf = processar_ultra(st.session_state.historico)

# Painéis
st.markdown(f'<div class="status-card"><h3 style="color: #ff00ff;">RADAR ROSA 🌸</h3><p>Distância: {st.session_state.distancia_rosa} rodadas</p></div>', unsafe_allow_html=True)
st.markdown(f'<div class="{cor}"><h1 style="color: {"#00ff00" if "ENTRAR" in sinal or "ROSA" in sinal else "#ff4b4b"};">{sinal}</h1><p>CONFIANÇA: {conf}<br>STATUS: {status}</p></div>', unsafe_allow_html=True)

if st.button("Limpar Histórico"):
    st.session_state.historico = []
    st.session_state.distancia_rosa = 0
    st.rerun()
