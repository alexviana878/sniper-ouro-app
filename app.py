import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="Sniper Ouro Mestre", page_icon="🎯", layout="centered")

# Estilo Neon de Luxo Preservado e Reforçado
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .clock-card { border: 1px solid #00ffff; border-radius: 10px; padding: 10px; text-align: center; background-color: #1a1c24; box-shadow: 0 0 5px #00ffff; margin-bottom: 10px; }
    .status-card { border: 2px solid #ff00ff; border-radius: 15px; padding: 15px; text-align: center; background-color: #1a1c24; box-shadow: 0 0 10px #ff00ff; }
    .target-card { border: 2px solid #00ff00; border-radius: 15px; padding: 15px; text-align: center; background-color: #1a1c24; box-shadow: 0 0 15px #00ff00; margin-top: 10px; }
    .wait-card { border: 2px solid #ff4b4b; border-radius: 15px; padding: 15px; text-align: center; background-color: #1a1c24; box-shadow: 0 0 10px #ff4b4b; margin-top: 10px; }
    .mentora-card { border: 1px dashed #ffff00; border-radius: 10px; padding: 10px; text-align: center; background-color: #22251a; box-shadow: 0 0 8px #ffff00; margin-top: 10px; color: #ffff00; font-weight: bold; }
    .janela-card { color: #00ffff; font-weight: bold; font-size: 18px; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

# Inicialização das Variáveis de Estado
if 'historico' not in st.session_state:
    st.session_state.historico = []
if 'distancia_rosa' not in st.session_state:
    st.session_state.distancia_rosa = 0
if 'contador_reset' not in st.session_state:
    st.session_state.contador_reset = -1 # -1 significa inativo
if 'contador_regra13' not in st.session_state:
    st.session_state.contador_regra13 = -1

# --- RELÓGIO E ANÁLISE DE TEMPO (CRONOS) ---
agora = datetime.now()
segundos = agora.second
janela_ativa = segundos >= 45 or segundos <= 15

# Painel do Relógio
st.markdown(f'<div class="clock-card"><h2 style="color: #00ffff; margin:0;">{agora.strftime("%H:%M:%S")}</h2>'
            f'<p class="janela-card">{"JANELA PAGANTE ATIVA ⏳" if janela_ativa else "AGUARDANDO MINUTO..."}</p></div>', unsafe_allow_html=True)

st.title("🎯 Sniper Ouro Mestre")

# Entrada de Dados
vela = st.number_input("Última Vela:", min_value=0.0, format="%.2f", step=0.01)

if st.button("ANALISAR PRÓXIMA"):
    st.session_state.historico.append(vela)
    
    # Atualiza distância da rosa tradicional
    st.session_state.distancia_rosa = 0 if vela >= 10.0 else st.session_state.distancia_rosa + 1
    
    # Lógica de contadores do E-book da Mentora
    if vela == 1.00:
        st.session_state.contador_reset = 0 # Inicia contagem de casas pós-reset
    elif st.session_state.contador_reset >= 0:
        st.session_state.contador_reset += 1
        
    if vela >= 30.00:
        st.session_state.contador_regra13 = 0 # Inicia Regra dos 13
    elif st.session_state.contador_regra13 >= 0:
        st.session_state.contador_regra13 += 1

# --- PROCESSAMENTO DOS ALERTAS DA MENTORA ---
avisos_mentora = []

if st.session_state.contador_reset >= 0:
    casa_atual = st.session_state.contador_reset
    if casa_atual <= 10:
        casas_fortes = [1, 4, 5, 8, 10]
        status_casa = "🔥 CASA FORTE!" if casa_atual in casas_fortes else "Aguardando próxima casa"
        avisos_mentora.append(f"🚨 RESET 1.00x Ativo: Casa {casa_atual}/10 ({status_casa})")
    else:
        st.session_state.contador_reset = -1 # Encerra o ciclo de 10 casas

if st.session_state.contador_regra13 >= 0:
    casa13_atual = st.session_state.contador_regra13
    if casa13_atual <= 15:
        casas_impares = [3, 5, 7, 9, 11, 13]
        status_13 = "🌸 ZONA IMPAR DE ROSA!" if casa13_atual in casas_impares else "Monitorando esteira"
        avisos_mentora.append(f"📏 REGRA DOS 13 Ativa: Casa {casa13_atual}/15 ({status_13})")
    else:
        st.session_state.contador_regra13 = -1

# --- ALGORITMO ULTRA COM ENGENHARIA REVERSA DE DECIMAIS ---
def processar_mestre(historico):
    if len(historico) < 3: 
        return "ANALISANDO...", "wait-card", "AGUARDANDO DADOS", "---"
    
    v_atual = historico[-1]
    
    # Verificação de gatilhos decimais do Cadeirola (E-book)
    decimal_string = f"{v_atual:.2f}"
    final_cinco = decimal_string.endswith('5')
    gatilho_5x = 1.64 <= v_atual <= 1.69
    gatilho_10x = 1.21 <= v_atual <= 1.29
    
    # Ajuste dinâmico de confiança baseado no e-book e tempo
    bônus_confiança = 0
    if janela_ativa: bônus_confiança += 3
    if final_cinco or gatilho_5x or gatilho_10x: bônus_confiança += 2
    
    # 1. Lógica Base de Quebra/Surf (Nossos Acertos)
    if all(x < 1.80 for x in historico[-3:-1]) and v_atual >= 1.80:
        conf_calc = min(98 + bônus_confiança, 99)
        return "ENTRAR (QUEBRA) 🎯", "target-card", "PADRÃO IDENTIFICADO", f"{conf_calc}%"
    
    # 2. Lógica Base de Maturação de Rosa (Nossos Acertos)
    if st.session_state.distancia_rosa > 12 and v_atual > 2.0:
        conf_calc = min(95 + bônus_confiança, 99)
        return "BUSCAR ROSA 🌸", "target-card", "MATURAÇÃO ALTA", f"{conf_calc}%"
    
    # 3. Lógica Base de Recuperação de Azul (Nossos Acertos)
    if v_atual < 2.0 and any(x >= 2.0 for x in historico[-4:-1]):
        conf_base = 92 + bônus_confiança
        return "ENTRAR (RECUPERAÇÃO) 🎯", "target-card", "CORREÇÃO DE GRÁFICO", f"{conf_base}%"

    # Alerta nativo para gatilhos diretos do e-book caso o gráfico não esteja em proteção
    if gatilho_10x or gatilho_5x or final_cinco:
        return "ENTRAR (GATILHO CADEIROLA) 🎯", "target-card", "DECIMAL INDICATIVA", "94%"

    if v_atual < 1.15: 
        return "AGUARDAR ✋", "wait-card", "MERCADO RECOLHEDOR", "99%"
        
    return "AGUARDAR ✋", "wait-card", "BUSCANDO GATILHO", "---"

sinal, cor, status, conf = processar_mestre(st.session_state.historico)

# Painel de Informações Operacionais
st.markdown(f'<div class="status-card"><h3 style="color: #ff00ff;">RADAR ROSA 🌸</h3><p>Distância: {st.session_state.distancia_rosa} rodadas</p></div>', unsafe_allow_html=True)

# Exibição de Alertas de Casas da Mentora (Apenas se houver gatilho ativo)
if avisos_mentora:
    for aviso in avisos_mentora:
        st.markdown(f'<div class="mentora-card">{aviso}</div>', unsafe_allow_html=True)

st.markdown(f'<div class="{cor}"><h1 style="color: {"#00ff00" if "ENTRAR" in sinal or "ROSA" in sinal else "#ff4b4b"};">{sinal}</h1><p>CONFIANÇA: {conf}<br>STATUS: {status}</p></div>', unsafe_allow_html=True)

# Botão de Reset de Sessão
if st.button("Limpar Histórico"):
    st.session_state.historico = []
    st.session_state.distancia_rosa = 0
    st.session_state.contador_reset = -1
    st.session_state.contador_regra13 = -1
    st.rerun()
