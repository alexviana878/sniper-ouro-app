import streamlit as st
from datetime import datetime

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Sniper Ouro IA PRO",
    page_icon="🎯",
    layout="centered"
)

# =========================================================
# LOGIN RESTRITO
# =========================================================
SENHA_CORRETA = "AlexMestre2026"

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align:center;color:#ef4444;'>🔒 SISTEMA PROTEGIDO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#888;'>Insira a chave master de laboratório.</p>", unsafe_allow_html=True)
    
    senha = st.text_input("Digite sua chave:", type="password")
    
    if st.button("ATIVAR SISTEMA"):
        if senha == SENHA_CORRETA:
            st.session_state.autenticado = True
            st.success("Sistema liberado.")
            st.rerun()
        else:
            st.error("Chave inválida.")
    st.stop()

# =========================================================
# CSS PREMIUM
# =========================================================
st.markdown("""
<style>
.stApp { background-color: #0d0e15; }
.status-card { border: 2px solid #a855f7; border-radius: 15px; padding: 15px; text-align: center; background-color: #111322; box-shadow: 0 0 15px #a855f7; color: white; margin-bottom: 15px; }
.target-card { border: 2px solid #00ff00; border-radius: 15px; padding: 15px; text-align: center; background-color: #111322; box-shadow: 0 0 18px #00ff00; color: white; margin-bottom: 15px; }
.wait-card { border: 2px solid #ef4444; border-radius: 15px; padding: 15px; text-align: center; background-color: #111322; box-shadow: 0 0 10px #ef4444; color: white; margin-bottom: 15px; }
.ranking-card { border: 2px solid #f59e0b; border-radius: 15px; padding: 15px; background-color: #111322; box-shadow: 0 0 12px #f59e0b; margin-top: 20px; color: white; }
.csv-card { border: 1px dashed #f59e0b; border-radius: 10px; padding: 15px; background-color: #1e1b4b; margin-bottom: 20px; }
.clock-card { border: 1px solid #00ff00; border-radius: 10px; padding: 10px; text-align: center; background-color: #111322; box-shadow: 0 0 5px #00ff00; margin-bottom: 15px; }
h1, h2, h3, p, label { color: white !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# INICIALIZAÇÃO DA MEMÓRIA VIVA (SESSION STATE)
# =========================================================
if "historico" not in st.session_state: st.session_state.historico = []
if "banco_padroes" not in st.session_state: st.session_state.banco_padroes = []
if "distancia_rosa" not in st.session_state: st.session_state.distancia_rosa = 0
if "acertos" not in st.session_state: st.session_state.acertos = 0
if "erros" not in st.session_state: st.session_state.erros = 0
if "ultima_entrada" not in st.session_state: st.session_state.ultima_entrada = None

# =========================================================
# RELÓGIO COGNITIVO
# =========================================================
agora = datetime.now()
minutos_pagantes = [2,5,8,10,12,15,18,20,22,25,28,30,32,35,38,40,42,45,48,50,52,55,58,0]
janela_ativa = agora.minute in minutos_pagantes

st.markdown(f"""
<div class="clock-card">
<h2 style="color:#00ff00 !important; margin:0;">{agora.strftime("%H:%M:%S")}</h2>
<p style="color:#00ff00 !important; margin:0;">{"⚠️ JANELA PAGANTE ATIVA" if janela_ativa else "MONITORANDO MERCADO"}</p>
</div>
""", unsafe_allow_html=True)

st.title("🎯 SNIPER OURO IA PRO")

# =========================================================
# 📂 NOVO ENGINE: IMPORTAÇÃO E TREINAMENTO EM MASSA VIA CSV
# =========================================================
st.markdown('<div class="csv-card">', unsafe_allow_html=True)
st.markdown("### 📂 IMPORTAR E TREINAR BASE DE DADOS")
arquivo = st.file_uploader("Envie seu arquivo histórico contendo as velas (1 por linha):", type=["csv", "txt"])

def classificar_vela(valor):
    if valor < 2.0: return "B"
    elif valor < 10.0: return "M"
    return "A"

def gerar_padrao(historico):
    if len(historico) < 4: return None
    return "-".join([classificar_vela(v) for v in historico[-4:]])

def salvar_padrao_na_memoria(padrao, resultado):
    st.session_state.banco_padroes.append({
        "padrao": padrao,
        "resultado": resultado
    })

if arquivo is not None:
    linhas = arquivo.read().decode("utf-8").splitlines()
    contador = 0
    
    # Processa e alimenta em massa de forma ultra veloz
    for linha in lines if 'lines' in locals() else linhas:
        try:
            limpo = linha.strip()
            if not limpo: continue
            valor = float(limpo.replace(",", "."))
            
            # Grava o padrão existente ANTES de embutir a nova vela
            if len(st.session_state.historico) >= 4:
                padrao_gerado = gerar_padrao(st.session_state.historico)
                salvar_padrao_na_memoria(padrao_gerado, valor)
                
            st.session_state.historico.append(valor)
            
            if valor >= 10.0: st.session_state.distancia_rosa = 0
            else: st.session_state.distancia_rosa += 1
            
            contador += 1
        except:
            pass
            
    st.success(f"🔥 Inteligência Alimentada! {contador} velas importadas com sucesso.")
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# FUNÇÕES DA ENGINE IA COGNITIVA
# =========================================================
def analisar_padroes():
    memoria = {}
    for registro in st.session_state.banco_padroes:
        padrao = registro["padrao"]
        resultado = registro["resultado"]

        if padrao not in memoria:
            memoria[padrao] = {"total": 0, "roxa": 0, "rosa": 0, "erro": 0}

        memoria[padrao]["total"] += 1
        if resultado >= 2.0: memoria[padrao]["roxa"] += 1
        else: memoria[padrao]["erro"] += 1
        if resultado >= 10.0: memoria[padrao]["rosa"] += 1
    return memoria

def calcular_score(historico, taxa_roxa, taxa_rosa):
    score = 0
    if len(historico) == 0: return 0
    v_atual = historico[-1]
    total_azuis = sum(1 for x in historico[-5:] if x < 2.0)

    if janela_ativa: score += 2
    if taxa_roxa >= 70: score += 4
    if taxa_roxa >= 85: score += 3
    if taxa_rosa >= 20: score += 3
    if st.session_state.distancia_rosa >= 12: score += 2
    if total_azuis <= 2: score += 2
    if total_azuis >= 4: score -= 5
    if v_atual < 1.15: score -= 4
    if len(historico) >= 2 and historico[-2] >= 2.0: score += 2
    return score

def processar_sinal(historico):
    if len(historico) < 10:
        return "ANALISANDO...", "wait-card", "ALIMENTANDO IA (MÍNIMO 10 VELAS)", "---", None

    padrao = gerar_padrao(historico)
    memoria = analisar_padroes()
    taxa_roxa, taxa_rosa, ocorrencias = 0.0, 0.0, 0

    if padrao in memoria:
        dados = memoria[padrao]
        ocorrencias = dados["total"]
        if ocorrencias > 0:
            taxa_roxa = (dados["roxa"] / ocorrencias) * 100
            taxa_rosa = (dados["rosa"] / ocorrencias) * 100

    score = calcular_score(historico, taxa_roxa, taxa_rosa)

    # =========================================================
    # CONFIGURAÇÃO PREMIUM EXIGENTE PRO CORRIGIDA (REGRA DE OURO)
    # =========================================================
    if score >= 14:
        return f"💎 ENTRADA PREMIUM ({padrao})", "target-card", f"PADRÃO ELITE CRÍTICO | ROXA {taxa_roxa:.1f}% | ROSA {taxa_rosa:.1f}% | SCORE {score}", f"{min(score * 7, 99)}%", "ROXA"
    if score >= 11:
        return f"⚠️ ENTRADA MODERADA ({padrao})", "status-card", f"PADRÃO BOM | ROXA {taxa_roxa:.1f}% | SCORE {score}", f"{min(score * 6, 92)}%", "ROXA"
    if taxa_rosa >= 30 and st.session_state.distancia_rosa >= 10:
        return f"🌸 BUSCAR ROSA ({padrao})", "target-card", f"PRESSÃO ESTATÍSTICA PARA ROSA | {taxa_rosa:.1f}%", "92%", "ROSA"
    
    return "AGUARDAR ✋", "wait-card", f"SEM CONFLUÊNCIA DE SCORE ALTO (SCORE ATUAL: {score})", "---", None

# =========================================================
# ENTRADA DE DADOS EM TEMPO REAL (OPERAÇÃO)
# =========================================================
banca = st.number_input("Banca Inicial (R$):", min_value=0.0, value=20.0, step=1.0)
vela = st.number_input("Digite a última vela:", min_value=0.0, format="%.2f", step=0.01)

if st.button("CALCULAR PROBABILIDADE"):
    if st.session_state.ultima_entrada == "ROXA":
        if vela >= 2.0: st.session_state.acertos += 1
        else: st.session_state.erros += 1
    elif st.session_state.ultima_entrada == "ROSA":
        if vela >= 10.0: st.session_state.acertos += 1
        else: st.session_state.erros += 1

    if len(st.session_state.historico) >= 4:
        padrao_gerado = gerar_padrao(st.session_state.historico)
        salvar_padrao_na_memoria(padrao_gerado, vela)

    st.session_state.historico.append(vela)

    if vela >= 10.0: st.session_state.distancia_rosa = 0
    else: st.session_state.distancia_rosa += 1

    st.rerun()

# EXECUÇÃO DO PROCESSO
sinal, cor, status, conf, entrada_gerada = processar_sinal(st.session_state.historico)
st.session_state.ultima_entrada = entrada_gerada

# EXIBIÇÃO DO PAINEL PRINCIPAL
st.markdown(f"""
<div class="{cor}">
<h1 style="margin:0; color: {'#00ff00' if 'ENTRADA' in sinal or 'BUSCAR' in sinal else '#ef4444'} !important;">{sinal}</h1>
<p style="margin:5px 0 0 0;"><b>CONFIANÇA MATEMÁTICA:</b> {conf}<br><b>DIRETRIZ:</b> {status}</p>
</div>
""", unsafe_allow_html=True)

# EXIBIÇÃO DO RADAR ROSA
st.markdown(f"""
<div class="status-card">
<h3 style="color:#a855f7 !important; margin:0;">🌸 RADAR ROSA</h3>
<p style="margin:5px 0 0 0;">Distância Atual: <b>{st.session_state.distancia_rosa}</b> rodadas sem velas altas</p>
</div>
""", unsafe_allow_html=True)

# SESSÃO REAL TIME RANKING
total_jogadas = st.session_state.acertos + st.session_state.erros
assertividade = (st.session_state.acertos / total_jogadas) * 100 if total_jogadas > 0 else 0.0

st.markdown('<div class="ranking-card">', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-weight:bold; color:#f59e0b !important; margin:0 0 10px 0;'>👑 PERFORMANCE DA SESSÃO IA PRO</p>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1: st.metric("✅ ACERTOS", st.session_state.acertos)
with col2: st.metric("❌ ERROS", st.session_state.erros)
with col3: st.metric("📊 ASSERTIVIDADE", f"{assertividade:.1f}%")
st.markdown("</div>", unsafe_allow_html=True)

# PAINEL DO REPOSITÓRIO TOP PADRÕES
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="ranking-card">
<h3 style='text-align:center; color:#00ff00 !important; margin:0 0 15px 0;'>🏆 TOP PADRÕES DO LABORATÓRIO</h3>
""", unsafe_allow_html=True)

memoria_mapeada = analisar_padroes()
padrões_filtrados = []

for pad, dados in memoria_mapeada.items():
    if dados["total"] >= 3: 
        taxa_sucesso = (dados["roxa"] / dados["total"]) * 100
        padrões_filtrados.append({"padrao": pad, "taxa": taxa_sucesso, "acertos": dados["roxa"], "total": dados["total"]})

padrões_filtrados = sorted(padrões_filtrados, key=lambda k: k['taxa'], reverse=True)[:5]

if padrões_filtrados:
    for item in padrões_filtrados:
        st.markdown(f"""
        <p style='color:white; margin:5px 0;'>
        💎 <b>{item['padrao']}</b> → <span style='color:#00ff00;'>{item['taxa']:.1f}%</span> de assertividade ({item['acertos']}/{item['total']})
        </p>
        """, unsafe_allow_html=True)
else:
    st.markdown("<p style='color:#888; text-align:center; margin:0;'>Suba o arquivo CSV de treinamento para mapear a inteligência preditiva.</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# MONITORAMENTO DA RETROALIMENTAÇÃO GRÁFICA
if len(st.session_state.historico) > 0:
    st.markdown("<p style='margin-top:15px;color:#888;'><b>Base de Dados Atualizada:</b> " + " → ".join([f"[{v}]" for v in st.session_state.historico[-12:]]) + "</p>", unsafe_allow_html=True)

# RESET DE SEGURANÇA
st.markdown("<br>", unsafe_allow_html=True)
if st.button("REINICIAR SISTEMA"):
    st.session_state.historico = []
    st.session_state.banco_padroes = []
    st.session_state.distancia_rosa = 0
    st.session_state.acertos = 0
    st.session_state.erros = 0
    st.session_state.ultima_entrada = None
    st.rerun()
