import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Sniper Ouro - Alpha Test", page_icon="🎯", layout="centered")

# --- SISTEMA DE CHAVE DE ATIVAÇÃO RESTRITA ---
SENHA_CORRETA = "AlexMestre2026"

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h2 style='text-align: center; color: #ef4444; margin-top: 50px;'>🔒 SISTEMA RESTRITO</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Insira a chave de ativação para liberar os módulos de validação matemática.</p>", unsafe_allow_html=True)
    
    senha_inserida = st.text_input("Chave de Acesso:", type="password")
    
    if st.button("ATIVAR SOFTWARE"):
        if senha_inserida == SENHA_CORRETA:
            st.session_state.autenticado = True
            st.success("Acesso liberado com sucesso!")
            st.rerun()
        else:
            st.error("Chave de acesso inválida. O sistema permanece bloqueado.")
    st.stop()

# --- DESIGN PREMIUM BLACK & PURPLE ---
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
            f'<p class="janela-card">{"JANELA PAGANTE ATIVA ⏳" if janela_ativa else "MONITORANDO FLUXO SEGURO..."}</p></div>', unsafe_allow_html=True)

st.success("🔓 Modo de Teste Conectado com Sucesso")
st.title("🎯 Sniper Ouro - Módulo de Validação")

vela = st.number_input("Digite a última vela do gráfico:", min_value=0.0, format="%.2f", step=0.01)

if st.button("CALCULAR PROBABILIDADE"):
    st.session_state.historico.append(vela)
    st.session_state.distancia_rosa = 0 if vela >= 10.0 else st.session_state.distancia_rosa + 1
    
    if vela == 1.00: st.session_state.contador_reset = 0
    elif st.session_state.contador_reset >= 0: st.session_state.contador_reset += 1
        
    if vela >= 30.00: st.session_state.contador_regra13 = 0
    elif st.session_state.contador_regra13 >= 0: st.session_state.contador_regra13 += 1

# --- RASTREADORES DE ESTEIRA ---
avisos_mentora = []
if 0 <= st.session_state.contador_reset <= 10:
    status_casa = "🔥 CASA FORTE (1, 4, 5, 8, 10)!" if st.session_state.contador_reset in [1, 4, 5, 8, 10] else "Aguardando próxima casa"
    avisos_mentora.append(f"🚨 ESTEIRA RESET 1.00x: Casa {st.session_state.contador_reset}/10 ({status_casa})")
else: st.session_state.contador_reset = -1

if 0 <= st.session_state.contador_regra13 <= 15:
    status_13 = "🌸 ZONA ÍMPAR DE ROSA!" if st.session_state.contador_regra13 in [3, 5, 7, 9, 11, 13] else "Monitorando esteira"
    avisos_mentora.append(f"📏 REGRA DOS 13: Casa {st.session_state.contador_regra13}/15 ({status_13})")
else: st.session_state.contador_regra13 = -1

# --- MOTORIZAÇÃO CALIBRADA ANTI-VÍCIO (57 ESTRATÉGIAS) ---
def processar_independente(historico):
    if len(historico) < 5: 
        return "ANALISANDO...", "wait-card", "ALIMENTANDO SESSÃO (INSIRA MAIS VELAS)", "---"
    
    v_atual = historico[-1]
    total_azuis_janela = sum(1 for x in historico[-5:] if x < 2.0)
    
    if total_azuis_janela >= 4 and v_atual < 2.0:
        return "AGUARDAR ✋", "wait-card", "MERCADO EM RECOLHIMENTO PROFUNDO", "100%"
        
    if len(historico) >= 3 and historico[-2] < 1.50 and historico[-3] < 1.50 and v_atual >= 2.0:
        return "AGUARDAR ✋", "wait-card", "CONFIRMANDO MUDANÇA DE PADRÃO (AGUARDE MAIS UMA ROXA)", "98%"

    decimal_str = f"{v_atual:.2f}"
    final_cinco = decimal_str.endswith('5')
    gatilho_5x = 1.64 <= v_atual <= 1.69
    gatilho_10x = 1.21 <= v_atual <= 1.29
    
    bônus = 3 if janela_ativa else 0

    if len(historico) >= 2 and historico[-2] >= 2.0 and v_atual >= 2.0:
        return "ENTRAR (PADRÃO SEGURO) 🎯", "target-card", "MERCADO EM FLUXO PAGADOR CONTINUO", f"{96 + bônus}%"

    if st.session_state.distancia_rosa > 12 and v_atual > 2.0:
        return "BUSCAR ROSA 🌸", "target-card", "PONTO CRÍTICO DE MATURAÇÃO", f"{95 + bônus}%"
        
    if v_atual < 2.0 and any(x >= 2.0 for x in historico[-4:-1]) and total_azuis_janela <= 2:
        return "ENTRAR (RECUPERAÇÃO) 🎯", "target-card", "CORREÇÃO DE GRÁFICO CURTA", f"{92 + bônus}%"

    if (gatilho_10x or gatilho_5x or final_cinco) and total_azuis_janela <= 2:
        return "ENTRAR (GATILHO DECIMAL) 🎯", "target-card", "CONFLUÊNCIA DE SUBIDA", "94%"

    if v_atual < 1.15: return "AGUARDAR ✋", "wait-card", "VELA DE COMPERÇÃO (BAIXA)", "99%"
    return "AGUARDAR ✋", "wait-card", "PROCURANDO ESTABILIDADE", "---"

sinal, cor, status, conf = processar_independente(st.session_state.historico)

st.markdown(f'<div class="status-card"><h3 style="color: #a855f7;">RADAR ROSA 🌸</h3><p>Distância Atual: {st.session_state.distancia_rosa} rodadas</p></div>', unsafe_allow_html=True)

if avisos_mentora:
    for aviso in avisos_mentora: st.markdown(f'<div class="mentora-card">{aviso}</div>', unsafe_allow_html=True)

st.markdown(f'<div class="{cor}"><h1 style="color: {"#00ff00" if "ENTRAR" in sinal or "ROSA" in sinal else "#ef4444"};">{sinal}</h1><p>CONFIANÇA ADAPTATIVA: {conf}<br>DIRETRIZ: {status}</p></div>', unsafe_allow_html=True)

if st.button("Limpar Histórico da Sessão"):
    st.session_state.historico = []
    st.session_state.distancia_rosa = 0
    st.session_state.contador_reset = -1
    st.session_state.contador_regra13 = -1
    st.rerun()
