import streamlit as st
from datetime import datetime
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import brain

st.set_page_config(page_title="Sniper Ouro Ecossistema IA", page_icon="🎯", layout="centered")

SENHA_CORRETA = "AlexMestre2026"
if "autenticado" not in st.session_state: st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align:center;color:#ef4444;'>🔒 ECOSSISTEMA SNIPER IA</h1>", unsafe_allow_html=True)
    senha = st.text_input("Digite sua chave master:", type="password")
    if st.button("ATIVAR ECOSSISTEMA"):
        if senha == SENHA_CORRETA:
            st.session_state.autenticado = True
            st.rerun()
        else: st.error("Senha inválida.")
    st.stop()

st.markdown("""
<style>
.stApp { background-color: #0d1117; }
.main-card { border: 2px solid #7c3aed; border-radius: 15px; padding: 15px; background-color: #111827; margin-bottom: 15px; box-shadow: 0 0 12px #7c3aed; color: white; }
.green-card { border: 2px solid #00ff66; border-radius: 15px; padding: 15px; background-color: #111827; margin-bottom: 15px; box-shadow: 0 0 15px #00ff66; color: white; }
.red-card { border: 2px solid #ef4444; border-radius: 15px; padding: 15px; background-color: #111827; margin-bottom: 15px; box-shadow: 0 0 12px #ef4444; color: white; }
.gold-card { border: 2px solid #f59e0b; border-radius: 15px; padding: 15px; background-color: #111827; margin-bottom: 15px; box-shadow: 0 0 12px #f59e0b; color: white; }
.blue-card { border: 2px solid #3b82f6; border-radius: 15px; padding: 15px; background-color: #111827; margin-bottom: 15px; box-shadow: 0 0 12px #3b82f6; color: white; }
.debug-card { border: 1px dashed #ff9900; border-radius: 10px; padding: 12px; background-color: #000000; margin-bottom: 15px; color: #ff9900; font-family: monospace; line-height: 1.5; }
.audit-card { border: 2px solid #00f0ff; border-radius: 12px; padding: 15px; background-color: #07111e; margin-bottom: 15px; box-shadow: 0 0 10px #00f0ff; color: white; }
.clock-card { border: 1px solid #00ff66; border-radius: 10px; padding: 10px; background-color: #111827; text-align: center; margin-bottom: 15px; }
h1,h2,h3,p,label { color: white !important; }
</style>
""", unsafe_allow_html=True)

ARQUIVO_MEMORIA = "memoria_sniper.json"

def carregar_memoria():
    if os.path.exists(ARQUIVO_MEMORIA):
        try:
            with open(ARQUIVO_MEMORIA, "r") as f:
                dados = json.load(f)
                # Garantir inicialização dos novos dicionários e listas de auditoria automatizada
                if "auditoria_freios" not in dados: dados["auditoria_freios"] = {"exaustao": 0, "degradacao": 0, "eficiencia": 0, "fase_macro": 0}
                if "auditoria_sinais" not in dados: dados["auditoria_sinais"] = {"CHANCE ELITE": 0, "ROSA ELITE": 0, "OBSERVANDO": 0, "AGUARDAR": 0, "OUTROS": 0}
                if "auditoria_assertividade" not in dados: dados["auditoria_assertividade"] = {"CHANCE ELITE": {"wins": 0, "loss": 0}, "ROSA ELITE": {"wins": 0, "loss": 0}, "OBSERVANDO": {"wins": 0, "loss": 0}, "AGUARDAR": {"wins": 0, "loss": 0}}
                if "log_auditoria_completo" not in dados: dados["log_auditoria_completo"] = []
                return dados
        except: pass
    return {
        "historico": [], "banco_padroes": [], "distancia_rosa": 0, 
        "acertos": 0, "erros": 0, "ultimos_resultados": [], 
        "quarentena": {}, "memoria_positiva": [], "memoria_negativa": {},
        "perdas_consecutivas": 0, "max_loss_streak": 0, "modo_defensivo": False, "cooldown_rodadas": 0, "sinais_ignorados": 0,
        "padroes_db": {}, "max_drawdown_calc": 0.0, "bloco_validacao": "NENHUM",
        "score_medio": 0, "total_operacoes": 0,
        "auditoria_freios": {"exaustao": 0, "degradacao": 0, "eficiencia": 0, "fase_macro": 0},
        "auditoria_sinais": {"CHANCE ELITE": 0, "ROSA ELITE": 0, "OBSERVANDO": 0, "AGUARDAR": 0, "OUTROS": 0},
        "auditoria_assertividade": {"CHANCE ELITE": {"wins": 0, "loss": 0}, "ROSA ELITE": {"wins": 0, "loss": 0}, "OBSERVANDO": {"wins": 0, "loss": 0}, "AGUARDAR": {"wins": 0, "loss": 0}},
        "log_auditoria_completo": []
    }

def salvar_memoria():
    dados = {
        "historico": st.session_state.historico, 
        "banco_padroes": st.session_state.banco_padroes, 
        "distancia_rosa": st.session_state.distancia_rosa, 
        "acertos": st.session_state.acertos, 
        "erros": st.session_state.erros, 
        "ultimos_resultados": st.session_state.ultimos_resultados, 
        "quarentena": st.session_state.quarentena,
        "memoria_positiva": st.session_state.memoria_positiva,
        "memoria_negativa": st.session_state.memoria_negativa,
        "perdas_consecutivas": st.session_state.perdas_consecutivas,
        "max_loss_streak": st.session_state.max_loss_streak,
        "modo_defensivo": st.session_state.modo_defensivo,
        "cooldown_rodadas": st.session_state.cooldown_rodadas,
        "sinais_ignorados": st.session_state.sinais_ignorados,
        "padroes_db": st.session_state.padroes_db,
        "max_drawdown_calc": st.session_state.max_drawdown_calc,
        "bloco_validacao": st.session_state.bloco_validacao,
        "score_medio": st.session_state.score_medio,
        "total_operacoes": st.session_state.total_operacoes,
        "auditoria_freios": st.session_state.auditoria_freios,
        "auditoria_sinais": st.session_state.auditoria_sinais,
        "auditoria_assertividade": st.session_state.auditoria_assertividade,
        "log_auditoria_completo": st.session_state.log_auditoria_completo
    }
    with open(ARQUIVO_MEMORIA, "w") as f: json.dump(dados, f)

if "dados_carregados" not in st.session_state:
    dados = carregar_memoria()
    st.session_state.historico = dados.get("historico", [])
    st.session_state.banco_padroes = dados.get("banco_padroes", [])
    st.session_state.distancia_rosa = dados.get("distancia_rosa", 0)
    st.session_state.acertos = dados.get("acertos", 0)
    st.session_state.erros = dados.get("erros", 0)
    st.session_state.ultimos_resultados = dados.get("ultimos_resultados", [])
    st.session_state.quarentena = dados.get("quarentena", {})
    st.session_state.memoria_positiva = dados.get("memoria_positiva", [])
    st.session_state.memoria_negativa = dados.get("memoria_negativa", {})
    st.session_state.perdas_consecutivas = dados.get("perdas_consecutivas", 0)
    st.session_state.max_loss_streak = dados.get("max_loss_streak", 0)
    st.session_state.modo_defensivo = dados.get("modo_defensivo", False)
    st.session_state.cooldown_rodadas = dados.get("cooldown_rodadas", 0)
    st.session_state.sinais_ignorados = dados.get("sinais_ignorados", 0)
    st.session_state.padroes_db = dados.get("padroes_db", {})
    st.session_state.max_drawdown_calc = dados.get("max_drawdown_calc", 0.0)
    st.session_state.bloco_validacao = dados.get("bloco_validacao", "NENHUM")
    st.session_state.score_medio = dados.get("score_medio", 0)
    st.session_state.total_operacoes = dados.get("total_operacoes", 0)
    
    # Acoplamento de Auditoria no Estado da Sessão
    st.session_state.auditoria_freios = dados.get("auditoria_freios", {"exaustao": 0, "degradacao": 0, "eficiencia": 0, "fase_macro": 0})
    st.session_state.auditoria_sinais = dados.get("auditoria_sinais", {"CHANCE ELITE": 0, "ROSA ELITE": 0, "OBSERVANDO": 0, "AGUARDAR": 0, "OUTROS": 0})
    st.session_state.auditoria_assertividade = dados.get("auditoria_assertividade", {"CHANCE ELITE": {"wins": 0, "loss": 0}, "ROSA ELITE": {"wins": 0, "loss": 0}, "OBSERVANDO": {"wins": 0, "loss": 0}, "AGUARDAR": {"wins": 0, "loss": 0}})
    st.session_state.log_auditoria_completo = dados.get("log_auditoria_completo", [])
    
    st.session_state.ultima_entrada = None
    st.session_state.ultimo_contexto = None
    st.session_state.dados_carregados = True

if st.session_state.quarentena:
    nova_quarentena = {}
    for ctx, rodadas in st.session_state.quarentena.items():
        nova = rodadas - 2
        if nova > 0: nova_quarentena[ctx] = nova
    st.session_state.quarentena = nova_quarentena

if st.session_state.modo_defensivo and st.session_state.cooldown_rodadas > 0:
    st.session_state.cooldown_rodadas -= 1
    if st.session_state.cooldown_rodadas <= 0:
        st.session_state.modo_defensivo = False
        st.session_state.perdas_consecutivas = 0

agora = datetime.now()
minutos_pagantes = [2,5,8,10,12,15,18,20,22,25,28,30,32,35,38,40,42,45,48,50,52,55,58,0]
janela_ativa = agora.minute in minutos_pagantes

st.markdown(f'<div class="clock-card"><h2 style="color:#00ff66 !important;margin:0;">{agora.strftime("%H:%M:%S")}</h2><p style="margin:0;color:#00ff66 !important;">{"⚠️ JANELA ATIVA DE EXPLOSÃO" if janela_ativa else "ECOSSISTEMA MONITORANDO"}</p></div>', unsafe_allow_html=True)

st.title("🎯 SNIPER OURO IA - LAB AUDITORIA QUANT G9")

with St.expander("📂 INJETAR DADOS / SELECIONAR BLOCO DE VALIDAÇÃO", expanded=False):
    bloco_opcao = st.radio("Escolha a partição de dados para testar sobrevivência:", ["Carga Completa (Sem Divisão)", "Bloco 1 (Velas 1 a 10.000)", "Bloco 2 (Velas 10.001 a 15.000 - Fora da Amostra)", "Bloco 3 (Velas 15.001 a 20.000 - Fora da Amostra)"])
    arquivo = st.file_uploader("Suba o arquivo master de dados", type=["csv","txt"])
    
    if arquivo is not None and len(st.session_state.historico) == 0:
        conteudo = arquivo.read().decode("utf-8")
        linhas = [ln.strip() for ln in conteudo.replace("\r", "\n").split("\n") if ln.strip()]
        dados_brutos = []
        for file_line in linhas:
            try:
                limpo = "".join([c for c in file_line if c.isdigit() or c in [".", ","]])
                if not limpo: continue
                dados_brutos.append(float(limpo.replace(",", ".")))
            except: pass
            
        if bloco_opcao == "Bloco 1 (Velas 1 a 10.000)":
            novo_historico = dados_brutos[:10000]
            st.session_state.bloco_validacao = "BLOCO 1 (TREINO)"
        elif bloco_opcao == "Bloco 2 (Velas 10.001 a 15.000 - Fora da Amostra)":
            novo_historico = dados_brutos[10000:15000]
            st.session_state.bloco_validacao = "BLOCO 2 (OUT-OF-SAMPLE)"
        elif bloco_opcao == "Bloco 3 (Velas 15.001 a 20.000 - Fora da Amostra)":
            novo_historico = dados_brutos[15000:20000]
            st.session_state.bloco_validacao = "BLOCO 3 (OUT-OF-SAMPLE)"
        else:
            novo_historico = dados_brutos
            st.session_state.bloco_validacao = "COMPLETO"

        novos_padroes, dist_rosa = [], 0
        for i, valor in enumerate(novo_historico):
            dist_rosa = 0 if valor >= 10 else dist_rosa + 1
            if i >= 5:
                novos_padroes.append({"padrao": brain.gerar_padrao(novo_historico[i-5:i]), "resultado": valor})
                
        st.session_state.historico = novo_historico
        st.session_state.banco_padroes = novos_padroes
        st.session_state.distancia_rosa = dist_rosa
        salvar_memoria()
        st.success(f"🔥 Laboratório Carregado: {len(novo_historico)} rodadas ativadas na partição {st.session_state.bloco_validacao}!")
        st.rerun()

def analisar_banco_avancado(padrao_alvo):
    total_p = wins_p = loss_p = 0
    resultados_recentes_padrao = []
    for reg in st.session_state.banco_padroes:
        if reg["padrao"] == padrao_alvo:
            total_p += 1
            if reg["resultado"] >= 2:
                wins_p += 1
                resultados_recentes_padrao.append(1)
            else:
                loss_p += 1
                resultados_recentes_padrao.append(0)
    winrate_historico = (wins_p / total_p) * 100 if total_p > 0 else 0.0
    janela_degradacao = resultados_recentes_padrao[-5:]
    winrate_recente = (janela_degradacao.count(1) / len(janela_degradacao)) * 100 if janela_degradacao else 100.0
    return total_p, winrate_historico, winrate_recente

def analisar_banco_global():
    memoria = {}
    for reg in st.session_state.banco_padroes:
        pad = reg["padrao"]
        if pad not in memoria: memoria[pad] = {"total": 0, "roxa": 0, "rosa": 0}
        memoria[pad]["total"] += 1
        if reg["resultado"] >= 2: memoria[pad]["roxa"] += 1
        if reg["resultado"] >= 10: memoria[pad]["rosa"] += 1
    return memoria

auditoria_dict = {"score_base": 0, "penalidade_fase": 0, "penalidade_eficiencia": 0, "penalidade_degradacao": 0, "penalidade_exaustao": 0}

if len(st.session_state.historico) >= 30:
    padrao_atual = brain.gerar_padrao(st.session_state.historico)
    fase_macro = brain.detectar_fase(st.session_state.historico)
    radar_score = brain.calcular_pressao_radar(st.session_state.historico, janela_ativa)
    expansion_score = brain.detectar_expansao(st.session_state.historico)
    aceleracoes = brain.detectar_aceleracao(st.session_state.historico)
    
    ocorrencias, winrate_padrao, winrate_recente_padrao = analisar_banco_avancado(padrao_atual)
    banco_global = analisar_banco_global()

    tx_roxa = 0
    if padrao_atual in banco_global:
        tx_roxa = (banco_global[padrao_atual]["roxa"] / ocorrencias) * 100 if ocorrencias > 0 else 0

    ultimas50 = st.session_state.historico[-50:]
    roxas_curto = sum(1 for x in ultimas50 if x >= 2)
    tx_roxa_quente_ctx = (roxas_curto / len(ultimas50)) * 100 if ultimas50 else 0.0
    
    adaptive_score, auditoria_dict = brain.calcular_score_adaptive(
        st.session_state.historico, tx_roxa, tx_roxa_quente_ctx, 
        ocorrencias, winrate_pad
