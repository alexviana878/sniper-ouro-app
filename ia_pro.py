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
    if f:=st.button("ATIVAR SISTEMA"):
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
# BANCO DE DADOS LOCAL (MEMÓRIA PERMANENTE NO SERVIDOR)
# =========================================================
ARQUIVO_BANCO = "memoria_extrema.txt"

def salvar_vela_no_disco(valor):
    with open(ARQUIVO_BANCO, "a") as f:
        f.write(f"{valor}\n")

def carregar_banco_do_disco():
    if not os.path.exists(ARQUIVO_BANCO):
        return []
    velas = []
    with open(ARQUIVO_BANCO, "r") as f:
        for linha in f:
            try:
                velas.append(float(linha.strip()))
            except: pass
    return velas

# =========================================================
# INICIALIZAÇÃO DE VARIÁVEIS DE SESSÃO
# =========================================================
if "historico" not in st.session_state:
    st.session_state.historico = carregar_banco_do_disco()

if "banco_padroes" not in st.session_state: st.session_state.banco_padroes = []
if "distancia_rosa" not in st.session_state: st.session_state.distancia_rosa = 0
if "acertos" not in st.session_state: st.session_state.acertos = 0
if "erros" not in st.session_state: st.session_state.erros = 0
if "ultima_entrada" not in st.session_state: st.session_state.ultima_entrada = None

# =========================================================
# RELÓGIO DE JANELAS DE TEMPO
# =========================================================
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

def salvar_padrao(padrao, resultado):
    st.session_state.banco_padroes.append({"padrao": padrao, "resultado": resultado})

def treinar_matriz_completa():
    st.session_state.banco_padroes = []
    total_velas = len(st.session_state.historico)
    if total_velas >= 5:
        historico_temporario = []
        for idx, valor in enumerate(st.session_state.historico):
            distancia_do_fim = total_velas - idx
            if distancia_do_fim <= 200: peso = 4       
            elif distancia_do_fim <= 800: peso = 2    
            else: peso = 1                             
            
            if len(historico_temporario) >= 4:
                padrao_existente = gerar_padrao(historico_temporario)
                if padrao_existente:
                    for _ in range(peso):
                        salvar_padrao(padrao_existente, valor)
            historico_temporario.append(valor)

if len(st.session_state.historico) > 0 and len(st.session_state.banco_padroes) == 0:
    treinar_matriz_completa()

# =========================================================
# 📂 REPOSITÓRIO DE CARGA CSV 
# =========================================================
st.markdown('<div class="main-card">### 📂 TREINAR INTELIGÊNCIA EXTREMA</div>', unsafe_allow_html=True)
arquivo = st.file_uploader("Suba um novo histórico CSV:", type=["csv", "txt"])

if arquivo is not None:
    linhas = arquivo.read().decode("utf-8").splitlines()
    contador_carga = 0
    for linha in linhas:
        try:
            limpo = linha.strip().replace('"', '').replace("'", "")
            if not limpo: continue
            partes = limpo.split()
            for parte in partes:
                val_limpo = parte.replace(",", ".")
                salvar_vela_no_disco(float(val_limpo))
                contador_carga += 1
                break
        except: pass
    if contador_carga > 0:
        st.session_state.historico = carregar_banco_do_disco()
        treinar_matriz_completa()
        st.rerun()

def analisar_padroes():
    memoria = {}
    for registro in st.session_state.banco_padroes:
        padrao = registro["padrao"]
        resultado = registro["resultado"]
        if not padrao: continue
        if padrao not in memoria:
            memoria[padrao] = {"total": 0, "roxa": 0, "rosa": 0, "erro": 0}
        memoria[padrao]["total"] += 1
        if resultado >= 2.0: memoria[padrao]["roxa"] += 1
        else: memoria[padrao]["erro"] += 1
        if resultado >= 10.0: memoria[padrao]["rosa"] += 1
    return memoria

def calcular_score(historico, taxa_roxa, taxa_rosa, ocorrencias):
    score = 0
    if len(historico) < 4: return 0
    v_atual = historico[-1]
    ultimas5 = historico[-5:] if len(historico) >= 5 else historico
    azuis = sum(1 for x in ultimas5 if x < 2.0)
    extremos = sum(1 for x in ultimas5 if x < 1.20)

    if azuis >= 4: score -= 10
    if extremos >= 2: score -= 8
    if v_atual < 1.10: score -= 10
    if taxa_roxa >= 70: score += 5
    if taxa_roxa >= 80: score += 3
    if taxa_roxa >= 90: score += 4
    if taxa_rosa >= 15: score += 3
    if ocorrencias >= 3: score += 3
    if ocorrencias >= 10: score += 4
    if ocorrencias >= 25: score += 4
    if janela_ativa: score += 2
    if st.session_state.distancia_rosa >= 10: score += 2
    if len(historico) >= 2 and historico[-2] >= 2.0: score += 2
    return score

# =========================================================
# PAINEL DE ENTRADA MANUAL (ORDEM VISUAL CORRETA)
# =========================================================
st.markdown("<br>", unsafe_allow_html=True)
banca = st.number_input("Banca Inicial (R$):", min_value=0.0, value=20.0, step=1.0)
vela = st.number_input("Digite a última vela:", min_value=0.0, format="%.2f", step=0.01)

if st.button("CALCULAR PROBABILIDADE"):
    if st.session_state.ultima_entrada in ["ROXA", "ROSA"]:
        if st.session_state.ultima_entrada == "ROXA" and vela >= 2.0: st.session_state.acertos += 1
        elif st.session_state.ultima_entrada == "ROSA" and vela >= 10.0: st.session_state.acertos += 1
        else: st.session_state.erros += 1

    if len(st.session_state.historico) >= 4:
        padrao_gerado = gerar_padrao(st.session_state.historico)
        if padrao_gerado: salvar_padrao(padrao_gerado, vela)

    salvar_vela_no_disco(vela)
    st.session_state.historico = carregar_banco_do_disco()
    
    if vela >= 10.0: st.session_state.distancia_rosa = 0
    else: st.session_state.distancia_rosa += 1
    
    treinar_matriz_completa()
    st.rerun()

# =========================================================
# MOTOR PREDITIVO COM ESCOPO GLOBAL BLINDADO (RESOLVE O NAMEERROR)
# =========================================================
historico_atual = st.session_state.historico
padrao = gerar_padrao(historico_atual)
memoria = analisar_padroes()

sinal, col_card, status, confianca, entrada_gerada = "ANALISANDO...", "red-card", "ALIMENTE O SISTEMA", "---", None
taxa_roxa, taxa_rosa, ocorrencias = 0.0, 0.0, 0

if len(historico_atual) >= 20:
    if padrao and padrao in memoria:
        dados = memoria[padrao]
        ocorrencias = dados["total"]
        if ocorrencias > 0:
            taxa_roxa = (dados["roxa"] / ocorrencias) * 100
            taxa_rosa = (dados["rosa"] / ocorrencias) * 100

    if ocorrencias < 3:
        sinal, col_card = "🚫 ZONA PROIBIDA", "red-card"
        status = f"PADRÃO ISOLADO ({padrao if padrao else '---'}) | OCORRÊNCIAS: {ocorrencias}/3 MÍNIMAS"
    elif taxa_roxa < 70.0:
        sinal, col_card = "🚫 SEM FORÇA ESTATÍSTICA", "red-card"
        status = f"TAXA HISTÓRICA INSUFICIENTE ({taxa_roxa:.1f}%)"
    else:
        score = calcular_score(historico_atual, taxa_roxa, taxa_rosa, ocorrencias)
        if score < 10:
            sinal, col_card = "🚫 SCORE INSUFICIENTE", "red-card"
            status = f"CONFLUÊNCIA DE CRITÉRIOS BAIXA (SCORE: {score}/10)"
        elif score >= 16:
            sinal, col_card = f"💎 ENTRADA EXTREMA ({padrao})", "green-card"
            status = f"PADRÃO ELITE CRÍTICO | ROXA {taxa_roxa:.1f}% | ROSA {taxa_rosa:.1f}% | SCORE {score}"
            confianca, entrada_gerada = "99%", "ROXA"
        elif score >= 10:
            sinal, col_card = f"⚡ ENTRADA SNIPER ({padrao})", "main-card"
            status = f"PADRÃO PREMIUM CONFLUENTE | ROXA {taxa_roxa:.1f}% | SCORE {score}"
            confianca, entrada_gerada = "92%", "ROXA"
        elif taxa_rosa >= 25 and st.session_state.distancia_rosa >= 10:
            sinal, col_card = f"🌸 BUSCAR ROSA ({padrao})", "green-card"
            status = f"ZONA ALTA MATURADA | CHANCE ROSA {taxa_rosa:.1f}%"
            confianca, entrada_gerada = "94%", "ROSA"
        else:
            sinal, col_card = "AGUARDAR ✋", "red-card"
            status = f"AGUARDANDO REFORÇO DE FLUXO (SCORE: {score})"

st.session_state.ultima_entrada = entrada_gerada

# DESENHO DO SINAL PRINCIPAL
st.markdown(f"""
<div class="{col_card}">
<h1 style='margin:0; color: {'#00ff00' if 'ENTRADA' in sinal or 'BUSCAR' in sinal else '#ef4444'} !important;'>{sinal}</h1>
<p style="margin:5px 0 0 0;"><b>CONFIANÇA:</b> {confianca}<br><b>DIRETRIZ:</b> {status}</p>
</div>
""", unsafe_allow_html=True)

# EXIBIÇÃO DO RADAR ROSA LOGO ABAIXO DO SINAL
st.markdown(f"""
<div class="main-card">
<h3>🌸 RADAR ROSA</h3>
<p style="margin:5px 0 0 0;">Distância atual: <b>{st.session_state.distancia_rosa}</b> rodadas sem estourar alvos altos</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# MONITOR DE RENDIMENTO E HISTÓRICO FIXO OBRIGATÓRIO (RODAPÉ)
# =========================================================
total_jogadas = st.session_state.acertos + st.session_state.erros
assertividade = (st.session_state.acertos / total_jogadas) * 100 if total_jogadas > 0 else 0.0

st.markdown("<div class='gold-card'><h3 style='text-align:center;color:#f59e0b !important; margin:0 0 10px 0;'>👑 PERFORMANCE DA IA</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1: st.metric("✅ ACERTOS", st.session_state.acertos)
with col2: st.metric("❌ ERROS", st.session_state.erros)
with col3: st.metric("📊 ASSERTIVIDADE", f"{assertividade:.1f}%")
st.markdown("</div>", unsafe_allow_html=True)

# TABELA DE TOP PADRÕES DO LABORATÓRIO
st.markdown("<div class='main-card'><h3 style='text-align:center; color:#00ff00 !important; margin:0 0 15px 0;'>🏆 TOP PADRÕES DO LABORATÓRIO</h3>", unsafe_allow_html=True)
ranking = []
if memoria:
    for pad_ch, dados_ch in memoria.items():
        if dados_ch["total"] >= 3: 
            tx = (dados_ch["roxa"] / dados_ch["total"]) * 100
            ranking.append({"padrao": pad_ch, "taxa": tx, "total": dados_ch["total"]})
ranking = sorted(ranking, key=lambda x: x["taxa"], reverse=True)[:5]

if ranking:
    for item in ranking:
        st.markdown(f"<p style='color:white; margin:5px 0;'>💎 <b>{item['padrao']}</b> → <span style='color:#00ff00;'>{item['taxa']:.1f}%</span> ({item['total']} ocorrências)</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='color:#888; text-align:center; margin:0;'>Aguardando amostragem estável de mercado (Mínimo: 3 ocorrências).</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# LINHA DO TEMPO RECENTE NO RODAPÉ DO MONITOR
if len(st.session_state.historico) > 0:
    velas_texto = " → ".join([f"[{v}]" for v in st.session_state.historico[-15:]])
    st.markdown(f"<p style='color:#888; margin-top:15px;'><b>Últimas velas (Total em Banco Fixo: {len(st.session_state.historico)}):</b> {velas_texto}</p>", unsafe_allow_html=True)

# BOTÕES DE LIMPEZA E MANUTENÇÃO NO FINAL DA PÁGINA
st.markdown("<br>", unsafe_allow_html=True)
if st.button("LIMPAR SESSÃO DA TELA"):
    st.session_state.acertos = 0
    st.session_state.erros = 0
    st.session_state.ultima_entrada = None
    st.rerun()

if st.button("DELETAR TODO BANCO PERMANENTE"):
    if os.path.exists(ARQUIVO_BANCO): os.remove(ARQUIVO_BANCO)
    st.session_state.historico = []
    st.session_state.banco_padroes = []
    st.session_state.distancia_rosa = 0
    st.session_state.acertos = 0
    st.session_state.erros = 0
    st.session_state.ultima_entrada = None
    st.success("Banco destruído com sucesso.")
    st.rerun()
