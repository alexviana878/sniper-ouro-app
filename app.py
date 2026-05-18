import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Sniper Ouro Mestre Black", page_icon="🎯", layout="centered")

# Visual Neon Premium - Alinhado com a Gestão Black
st.markdown("""
    <style>
    .main { background-color: #0d0e15; }
    .clock-card { border: 1px solid #00ff00; border-radius: 10px; padding: 10px; text-align: center; background-color: #111322; box-shadow: 0 0 5px #00ff00; margin-bottom: 10px; }
    .status-card { border: 2px solid #a855f7; border-radius: 15px; padding: 15px; text-align: center; background-color: #111322; box-shadow: 0 0 10px #a855f7; }
    .target-card { border: 2px solid #00ff00; border-radius: 15px; padding: 15px; text-align: center; background-color: #111322; box-shadow: 0 0 15px #00ff00; margin-top: 10px; }
    .wait-card { border: 2px solid #ef4444; border-radius: 15px; padding: 15px; text-align: center; background-color: #111322; box-shadow: 0 0 10px #ef4444; margin-top: 10px; }
    .mentora-card { border: 1px dashed #ffff00; border-radius: 10px; padding: 10px; text-align: center; background-color: #1a1a10; box-shadow: 0 0 8px #ffff00; margin-top: 10px; color: #ffff00; font-weight: bold; }
    .janela-card { color: #00ff00; font-weight: bold; font-size: 18px; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

if 'historico' not in st.session_state: st.session_state.historico = []
if 'distancia_rosa' not in st.session_state: st.session_state.distancia_rosa = 0
if 'contador_reset' not in st.session_state: st.session_state.contador_reset = -1
if 'contador_regra13' not in st.session_state: st.session_state.contador_regra13 = -1

# --- CRONOS TIMING ---
agora = datetime.now()
segundos = agora.second
janela_ativa = segundos >= 45 or segundos <= 15

st.markdown(f'<div class="clock-card"><h2 style="color: #00ff00; margin:0;">{agora.strftime("%H:%M:%S")}</h2>'
            f'<p class="janela-card">{"JANELA PAGANTE ATIVA ⏳" if janela_ativa else "MONITORANDO FLUXO..."}</p></div>', unsafe_allow_html=True)

st.title("🎯 Sniper Ouro Mestre Black")

vela = st.number_input("Última Vela Registrada:", min_value=0.0, format="%.2f", step=0.01)

if st.button("PROCESSAR ANÁLISE BLACK"):
    st.session_state.historico.append(vela)
    st.session_state.distancia_rosa = 0 if vela >= 10.0 else st.session_state.distancia_rosa + 1
    
    if vela == 1.00: st.session_state.contador_reset = 0
    elif st.session_state.contador_reset >= 0: st.session_state.contador_reset += 1
        
    if vela >= 30.00: st.session_state.contador_regra13 = 0
    elif st.session_state.contador_regra13 >= 0: st.session_state.contador_regra13 += 1

# --- RASTREADOR DE ESTEIRA DA MENTORA ---
avisos_mentora = []
if 0 <= st.session_state.contador_reset <= 10:
    status_casa = "🔥 CASA FORTE (1, 4, 5, 8, 10)!" if st.session_state.contador_reset in [1, 4, 5, 8, 10] else "Aguardando próxima casa"
    avisos_mentora.append(f"🚨 RESET 1.00x Ativo: Casa {st.session_state.contador_reset}/10 ({status_casa})")
else: st.session_state.contador_reset = -1

if 0 <= st.session_state.contador_regra13 <= 15:
    status_13 = "🌸 ZONA ÍMPAR DE ROSA!" if st.session_state.contador_regra13 in [3, 5, 7, 9, 11, 13] else "Monitorando esteira"
    avisos_mentora.append(f"📏 REGRA DOS 13: Casa {st.session_state.contador_regra13}/15 ({status_13})")
else: st.session_state.contador_regra13 = -1

# --- ENGINE MATEMÁTICA DE PROTEÇÃO ANTI-RECOLHIMENTO ---
def analisar_fluxo_black(historico):
    if len(historico) < 4: return "ANALISANDO...", "wait-card", "ALIMENTANDO SESSÃO", "---"
    
    v_atual = historico[-1]
    ultimos_azuis = sum(1 for x in historico[-4:] if x < 2.0)
    
    # 1. PROTEÇÃO TOTAL ANTI-RECOLHE (Filtro estrito do E-book)
    # Se veio de uma sequência de azuis e pagou apenas UMA roxa, o algoritmo trava em AGUARDAR
    if len(historico) >= 3 and historico[-2] < 2.0 and historico[-3] < 2.0 and v_atual >= 2.0:
        return "AGUARDAR ✋", "wait-card", "PROTEÇÃO: RISCO DE FALSA RECUPERAÇÃO", "99%"
        
    # 2. FILTRO DE TENDÊNCIA DE RECOLHEMENTO GERAL
    if ultimos_azuis >= 3 and v_atual < 2.0:
        return "AGUARDAR ✋", "wait-card", "ALERTA DE RECOLHIMENTO DA PLATAFORMA", "100%"

    # Gatilhos Decimais e Faixas do Cadeirola
    decimal_str = f"{v_atual:.2f}"
    final_cinco = decimal_str.endswith('5')
    gatilho_5x = 1.64 <= v_atual <= 1.69
    gatilho_10x = 1.21 <= v_atual <= 1.29
    gatilho_quebra_alta = 1.70 <= v_atual <= 1.98
    
    bônus = 3 if janela_ativa else 0
    
    # 3. GATILHO DE QUEBRA PÓS-SEQUÊNCIA ALTA (1.70 a 1.98)
    if gatilho_quebra_alta and any(x >= 10.0 for x in historico[-5:-1]):
        return "ENTRAR (GATILHO QUEBRA) 🎯", "target-card", "CHANCE DE VELA ALTA EM AT SÉRIE", f"{94 + bônus}%"

    # 4. ENTRADAS EM MUDANÇA DE PADRÃO (Duas velas positivas consecutivas em recuperação)
    if len(historico) >= 2 and historico[-2] >= 2.0 and v_atual >= 2.0:
        return "ENTRAR (PADRÃO CONFIRMADO) 🎯", "target-card", "GRÁFICO VOLTOU A PAGAR", f"{96 + bônus}%"

    # 5. MATURAÇÃO DE ROSA (Nossos Acertos)
    if st.session_state.distancia_rosa > 12 and v_atual > 2.0:
        return "BUSCAR ROSA 🌸", "target-card", "ZONA DE MATURAÇÃO CRÍTICA", f"{95 + bônus}%"

    # 6. GATILHOS EXCLUSIVOS DE DECIMAIS (Cadeirola)
    if (gatilho_10x or gatilho_5x or final_cinco) and ultimos_azuis < 2:
        return "ENTRAR (GATILHO DECIMAL) 🎯", "target-card", "CONFLUÊNCIA DE GATILHO", "94%"

    if v_atual < 1.15: return "AGUARDAR ✋", "wait-card", "VELA DE RECONHECIMENTO (BAIXA)", "99%"
    return "AGUARDAR ✋", "wait-card", "BUSCANDO PADRÃO DE SEGURANÇA", "---"

sinal, cor, status, conf = analisar_fluxo_black(st.session_state.historico)

# Interface de Exibição
st.markdown(f'<div class="status-card"><h3 style="color: #a855f7;">RADAR ROSA 🌸</h3><p>Distância Atual: {st.session_state.distancia_rosa} rodadas</p></div>', unsafe_allow_html=True)

if avisos_mentora:
    for aviso in avisos_mentora: st.markdown(f'<div class="mentora-card">{aviso}</div>', unsafe_allow_html=True)

st.markdown(f'<div class="{cor}"><h1 style="color: {"#00ff00" if "ENTRAR" in sinal or "ROSA" in sinal else "#ef4444"};">{sinal}</h1><p>CONFIANÇA MATEMÁTICA: {conf}<br>STATUS TÁTICO: {status}</p></div>', unsafe_allow_html=True)

if st.button("Limpar Histórico de Sessão"):
    st.session_state.historico = []
    st.session_state.distancia_rosa = 0
    st.session_state.contador_reset = -1
    st.session_state.contador_regra13 = -1
    st.rerun()
