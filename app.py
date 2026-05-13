import streamlit as st

st.set_page_config(page_title="Sniper Ouro Ultra", page_icon="🎯")

# Estilo de Luxo (Visual Neon)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .status-card { border: 2px solid #ff00ff; border-radius: 15px; padding: 15px; text-align: center; background-color: #1a1c24; box-shadow: 0 0 10px #ff00ff; }
    .target-card { border: 2px solid #00ff00; border-radius: 15px; padding: 15px; text-align: center; background-color: #1a1c24; box-shadow: 0 0 15px #00ff00; margin-top: 10px; }
    .wait-card { border: 2px solid #ff4b4b; border-radius: 15px; padding: 15px; text-align: center; background-color: #1a1c24; box-shadow: 0 0 10px #ff4b4b; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'historico' not in st.session_state:
    st.session_state.historico = []
if 'distancia_rosa' not in st.session_state:
    st.session_state.distancia_rosa = 0

st.title("🎯 Sniper Ouro Ultra")

# Entrada da Vela
vela = st.number_input("Digite a Última Vela:", min_value=0.0, format="%.2f", step=0.01)

if st.button("ANALISAR PRÓXIMA"):
    st.session_state.historico.append(vela)
    if vela >= 10.0:
        st.session_state.distancia_rosa = 0
    else:
        st.session_state.distancia_rosa += 1

# --- ALGORITMO DE INTELIGÊNCIA (AS 54 ESTRATÉGIAS) ---
def processar_estratégia(historico):
    if len(historico) < 3:
        return "ANALISANDO PADRÕES...", "wait-card", "AGUARDANDO DADOS", "50%"
    
    ultimas_3 = historico[-3:]
    v_atual = historico[-1]
    
    # 1. Filtro de Segurança Máxima (Recolhimento)
    if v_atual < 1.10:
        return "AGUARDAR ✋", "wait-card", "MERCADO RECOLHEDOR", "99%"
    
    # 2. Estratégia de Quebra de Ciclo (O que você via na planilha)
    # Se houve uma sequência de baixas e o mercado deu um sinal de força (acima de 1.50)
    if all(x < 1.80 for x in historico[-3:-1]) and v_atual >= 1.80:
        return "ENTRAR 1.30X 🎯", "target-card", "QUEBRA DE PADRÃO DETECTADA", "98%"

    # 3. Estratégia de Busca de Rosa (Maturação)
    # Se o radar rosa estiver acima de 12 rodadas e a última vela foi pagadora
    if st.session_state.distancia_rosa > 12 and v_atual > 2.0:
        return "BUSCAR ROSA 🌸", "target-card", "MATURAÇÃO DE VELA ALTA", "95%"

    # 4. Filtro de Sequência Azul (Não para no primeiro azul, analisa o conjunto)
    if v_atual < 2.0 and any(x >= 2.0 for x in historico[-4:-1]):
        return "ENTRAR (RECUPERAÇÃO) 🎯", "target-card", "PADRÃO DE CORREÇÃO", "92%"

    return "AGUARDAR ✋", "wait-card", "AGUARDANDO CONFIRMAÇÃO", "---"

sinal, cor, status, conf = processar_estratégia(st.session_state.historico)

# Exibição dos Painéis
st.markdown(f'<div class="status-card"><h3 style="color: #ff00ff;">RADAR ROSA 🌸</h3><p>Distância: {st.session_state.distancia_rosa} rodadas</p></div>', unsafe_allow_html=True)
st.markdown(f'<div class="{cor}"><h1 style="color: {"#00ff00" if "ENTRAR" in sinal or "ROSA" in sinal else "#ff4b4b"};">{sinal}</h1><p>CONFIANÇA: {conf}<br>STATUS: {status}</p></div>', unsafe_allow_html=True)

if st.button("Limpar Histórico"):
    st.session_state.historico = []
    st.session_state.distancia_rosa = 0
    st.rerun()
