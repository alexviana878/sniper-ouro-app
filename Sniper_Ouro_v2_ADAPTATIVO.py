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

with st.expander("📂 INJETAR DADOS / SELECIONAR BLOCO DE VALIDAÇÃO", expanded=False):
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
    
    retorno_adaptive = brain.calcular_score_adaptive(
        st.session_state.historico, tx_roxa, tx_roxa_quente_ctx, 
        ocorrencias, winrate_padrao, winrate_recente_padrao, 
        st.session_state.ultimos_resultados, janela_ativa
    )
    
    if isinstance(retorno_adaptive, tuple):
        adaptive_score, auditoria_dict = retorno_adaptive
    else:
        adaptive_score = retorno_adaptive
        auditoria_dict = {"score_base": adaptive_score, "penalidade_fase": 0, "penalidade_eficiencia": 0, "penalidade_degradacao": 0, "penalidade_exaustao": 0}
    
    if st.session_state.distancia_rosa <= 5: faixa_rosa = "CURTA"
    elif st.session_state.distancia_rosa <= 12: faixa_rosa = "MEDIA"
    else: faixa_rosa = "LONGA"
    
    contexto_chave = f"{padrao_atual}_{fase_macro}_{faixa_rosa}"
    if contexto_chave in st.session_state.memoria_positiva: adaptive_score = min(adaptive_score + 8, 100)
    if contexto_chave in st.session_state.quarentena: adaptive_score = max(adaptive_score - min(st.session_state.quarentena[contexto_chave] * 2, 30), 0)
    
    adaptive_score -= min(st.session_state.memoria_negativa.get(contexto_chave, 0) * 2.5, 25)
    mercado_instavel = tx_roxa_quente_ctx < 38 and radar_score < 45 and expansion_score < 45
    
    if aceleracoes["roxa"]: radar_score = min(radar_score + 4, 100)
    if aceleracoes["rosa"]: expansion_score = min(expansion_score + 6, 100)
    
    adaptive_score = max(min(adaptive_score, 100), 0)
    sinal_final, score_final = brain.calcular_consenso(adaptive_score, radar_score, expansion_score, fase_macro, tx_roxa_quente_ctx, mercado_instavel, st.session_state.historico, winrate_padrao, winrate_recente_padrao)
    
    if "ELITE" in sinal_final and score_final < 68: score_final = 68
    if st.session_state.modo_defensivo and st.session_state.cooldown_rodadas > 0:
        sinal_final = "🚫 COOLDOWN SHIELD"
        score_final = 0
        
    rm = brain.RiskManager()
    risco_ruina_status = rm.calcular_risco_ruina(st.session_state.acertos, st.session_state.erros, st.session_state.max_loss_streak)
    densidade_roxa_v = sum(1 for x in st.session_state.historico[-15:] if x >= 2) if len(st.session_state.historico) >= 15 else 0
        
    st.session_state.ultima_entrada = sinal_final
    st.session_state.ultimo_contexto = contexto_chave
else:
    sinal_final, score_final, expansion_score, radar_score, fase_macro, ocorrencias, tx_roxa, tx_roxa_quente_ctx, padrao_atual, adaptive_score = "COLETANDO DADOS", 0, 0, 0, "NEUTRA", 0, 0, 0, "---", 0
    winrate_padrao = winrate_recente_padrao = 100.0
    risco_ruina_status = "COLETANDO"
    densidade_roxa_v = 0

st.markdown(f'<div class="main-card"><p style="margin:0;text-align:center;color:#7c3aed;font-size:14px;"><b>PARTIÇÃO ATIVA:</b> {st.session_state.bloco_validacao}</p></div>', unsafe_allow_html=True)

st.markdown('<div class="main-card"><h3>🎮 PAINEL DE COMANDO AO VIVO</h3></div>', unsafe_allow_html=True)
vela = st.number_input("Digite o resultado da última rodada:", min_value=0.0, format="%.2f", step=0.01)

if st.button("PROCESSAR E CALCULAR PROBABILIDADE"):
    if st.session_state.ultimo_contexto:
        sinal_ativo = st.session_state.ultima_entrada
        if "ROSA" in sinal_ativo: deu_green = vela >= 10
        else: deu_green = vela >= 2
            
        nome_sinal_limpo = "CHANCE ELITE" if "CHANCE ELITE" in sinal_ativo else ("ROSA ELITE" if "ROSA ELITE" in sinal_ativo else ("OBSERVANDO" if "OBSERVANDO" in sinal_ativo else "AGUARDAR"))
        st.session_state.auditoria_sinais[nome_sinal_limpo] += 1
        
        if auditoria_dict.get("penalidade_exaustao", 0) > 0: st.session_state.auditoria_freios["exaustao"] += 1
        if auditoria_dict.get("penalidade_degradacao", 0) > 0: st.session_state.auditoria_freios["degradacao"] += 1
        if auditoria_dict.get("penalidade_eficiencia", 0) > 0: st.session_state.auditoria_freios["eficiencia"] += 1
        if auditoria_dict.get("penalidade_fase", 0) > 0: st.session_state.auditoria_freios["fase_macro"] += 1
        
        if nome_sinal_limpo in st.session_state.auditoria_assertividade:
            if deu_green: st.session_state.auditoria_assertividade[nome_sinal_limpo]["wins"] += 1
            else: st.session_state.auditoria_assertividade[nome_sinal_limpo]["loss"] += 1

        st.session_state.log_auditoria_completo.append({
            "rodada": len(st.session_state.historico) + 1,
            "padrao": padrao_atual,
            "sinal": nome_sinal_limpo,
            "score_adaptive": adaptive_score,
            "exaustao": auditoria_dict.get("penalidade_exaustao", 0) > 0,
            "degradacao": auditoria_dict.get("penalidade_degradacao", 0) > 0,
            "eficiencia": auditoria_dict.get("penalidade_eficiencia", 0) > 0,
            "fase_macro": auditoria_dict.get("penalidade_fase", 0) > 0,
            "resultado_vela": vela,
            "resultado_status": "WIN" if deu_green else "LOSS"
        })

        if ("ELITE" in sinal_ativo or "CHANCE" in sinal_ativo or "ROSA" in sinal_ativo):
            st.session_state.total_operacoes += 1
            st.session_state.score_medio = int(((st.session_state.score_medio * (st.session_state.total_operacoes - 1)) + score_final) / st.session_state.total_operacoes)
            
            if padrao_atual not in st.session_state.padroes_db: st.session_state.padroes_db[padrao_atual] = {"wins": 0, "loss": 0, "ultimo_winrate": 0.0}
            if not deu_green:
                st.session_state.quarentena[st.session_state.ultimo_contexto] = 15 if "ROSA" in sinal_ativo else 45
                st.session_state.erros += 1
                st.session_state.ultimos_resultados.append("LOSS")
                st.session_state.perdas_consecutivas += 1
                st.session_state.padroes_db[padrao_atual]["loss"] += 1
                if st.session_state.perdas_consecutivas >= 4:
                    st.session_state.modo_defensivo = True
                    st.session_state.cooldown_rodadas = 15
                if st.session_state.ultimo_contexto not in st.session_state.memoria_negativa: st.session_state.memoria_negativa[st.session_state.ultimo_contexto] = 0
                st.session_state.memoria_negativa[st.session_state.ultimo_contexto] += 1
            else:
                if len(st.session_state.memoria_positiva) >= 300: st.session_state.memoria_positiva.pop(0)
                if st.session_state.ultimo_contexto not in st.session_state.memoria_positiva: st.session_state.memoria_positiva.append(st.session_state.ultimo_contexto)
                st.session_state.acertos += 1
                st.session_state.ultimos_resultados.append("WIN")
                st.session_state.perdas_consecutivas = 0
                st.session_state.modo_defensivo = False
                st.session_state.cooldown_rodadas = 0
                st.session_state.padroes_db[padrao_atual]["wins"] += 1
                
            st.session_state.padroes_db[padrao_atual]["ultimo_winrate"] = round((st.session_state.padroes_db[padrao_atual]["wins"] / (st.session_state.padroes_db[padrao_atual]["wins"] + st.session_state.padroes_db[padrao_atual]["loss"])) * 100, 1)
                
        saldo = 1000.0 + (st.session_state.acertos * 10.0) - (st.session_state.erros * 10.0)
        dd_atual = (1000.0 - saldo) / 1000.0 if saldo < 1000.0 else 0.0
        if dd_atual > st.session_state.max_drawdown_calc: st.session_state.max_drawdown_calc = dd_atual
        if len(st.session_state.ultimos_resultados) > 50: st.session_state.ultimos_resultados.pop(0)

    if len(st.session_state.historico) >= 5: st.session_state.banco_padroes.append({"padrao": brain.gerar_padrao(st.session_state.historico), "resultado": vela})
    st.session_state.historico.append(vela)
    st.session_state.distancia_rosa = 0 if vela >= 10 else st.session_state.distancia_rosa + 1
    if st.session_state.perdas_consecutivas > st.session_state.max_loss_streak: st.session_state.max_loss_streak = st.session_state.perdas_consecutivas
        
    salvar_memoria()
    st.rerun()

cor_card = "red-card"
if "CHANCE ELITE" in sinal_final: cor_card = "green-card"
elif "ROSA ELITE" in sinal_final: cor_card = "blue-card"
elif "OBSERVANDO" in sinal_final: cor_card = "gold-card"

st.markdown(f'<div class="{cor_card}"><h1 style="text-align:center;font-size:38px;margin:0;">{sinal_final}</h1><p style="text-align:center;margin:5px 0 0 0;font-size:18px;"><b>CONSENSO:</b> {score_final}% | <b>PADRÃO:</b> {padrao_atual}</p></div>', unsafe_allow_html=True)

st.markdown("""
<div class="debug-card">
    • 🧱 BASE STRUCTURAL SCORE : <b>{} pts</b><br>
    • 🛑 PENALIDADE EXAUSTÃO  : <span style="color:#ff3333;"><b>-{} pts</b></span> | • 🥀 PENALIDADE DEGRADAÇÃO: <span style="color:#ff3333;"><b>-{} pts</b></span><br>
    • 🛡️ PENALIDADE EFICIÊNCIA: <span style="color:#ff3333;"><b>-{} pts</b></span> | • 🛡️ PENALIDADE FASE MACRO: <span style="color:#ff3333;"><b>-{} pts</b></span><br>
    <hr style="margin:5px 0; border:0; border-top:1px dashed #ff9900;">
    • 🧬 CORE ADAPTIVE FINAL  : <b>{}%</b>
</div>
""".format(
    auditoria_dict.get("score_base", 0), 
    auditoria_dict.get("penalidade_exaustao", 0), 
    auditoria_dict.get("penalidade_degradacao", 0), 
    auditoria_dict.get("penalidade_eficiencia", 0), 
    auditoria_dict.get("penalidade_fase", 0), 
    adaptive_score
), unsafe_allow_html=True)

st.markdown('<div class="audit-card"><h3>📊 RELATÓRIO DE AUDITORIA QUANTITATIVA AUTOMÁTICA</h3></div>', unsafe_allow_html=True)
total_rodadas_auditadas = len(st.session_state.log_auditoria_completo)
total_rodadas_historico = len(st.session_state.historico)

# LINHA ADICIONADA: Exibe o somatório acumulado do histórico (Carga + Digitadas)
st.markdown(f"📊 **Volume Total do Histórico Ativo:** `{total_rodadas_historico}` rodadas carregadas no ecossistema.")
st.write(f"🧬 *Volume de Amostragem Auditada nesta Sessão:* **{total_rodadas_auditadas}** rodadas gravadas automaticamente.")

col_f1, col_f2 = st.columns(2)
with col_f1:
    st.markdown("##### 🛑 Atuações de Freios Internos")
    st.markdown(f"• **Exaustão:** `{st.session_state.auditoria_freios['exaustao']}` acionamentos")
    st.markdown(f"• **Degradação Recente:** `{st.session_state.auditoria_freios['degradacao']}` acionamentos")
    st.markdown(f"• **Eficiência:** `{st.session_state.auditoria_freios['eficiencia']}` acionamentos")
    st.markdown(f"• **Fase Macro:** `{st.session_state.auditoria_freios['fase_macro']}` acionamentos")

with col_f2:
    st.markdown("##### 📢 Distribuição de Volumetria de Sinais")
    st.markdown(f"• **CHANCE ELITE:** `{st.session_state.auditoria_sinais['CHANCE ELITE']}` vezes")
    st.markdown(f"• **ROSA ELITE:** `{st.session_state.auditoria_sinais['ROSA ELITE']}` vezes")
    st.markdown(f"• **OBSERVANDO:** `{st.session_state.auditoria_sinais['OBSERVANDO']}` vezes")
    st.markdown(f"• **AGUARDAR:** `{st.session_state.auditoria_sinais['AGUARDAR']}` vezes")

st.markdown("##### 🎯 Raio-X de Assertividade por Classificação")
c_as1, c_as2, c_as3, c_as4 = st.columns(4)
with c_as1:
    ce_w = st.session_state.auditoria_assertividade["CHANCE ELITE"]["wins"]
    ce_l = st.session_state.auditoria_assertividade["CHANCE ELITE"]["loss"]
    st.metric("CHANCE ELITE", f"{ce_w}W - {ce_l}L", f"Total: {ce_w+ce_l}")
with c_as2:
    re_w = st.session_state.auditoria_assertividade["ROSA ELITE"]["wins"]
    re_l = st.session_state.auditoria_assertividade["ROSA ELITE"]["loss"]
    st.metric("ROSA ELITE", f"{re_w}W - {re_l}L", f"Total: {re_w+re_l}")
with c_as3:
    ob_w = st.session_state.auditoria_assertividade["OBSERVANDO"]["wins"]
    ob_l = st.session_state.auditoria_assertividade["OBSERVANDO"]["loss"]
    st.metric("OBSERVANDO", f"{ob_w}W - {ob_l}L", f"Total: {ob_w+ob_l}")
with c_as4:
    ag_w = st.session_state.auditoria_assertividade["AGUARDAR"]["wins"]
    ag_l = st.session_state.auditoria_assertividade["AGUARDAR"]["loss"]
    st.metric("AGUARDAR", f"{ag_w}W - {ag_l}L", f"Total: {ag_w+ag_l}")

if total_rodadas_auditadas > 0:
    with st.expander("📥 VER BANCO DATA LOG COMPLETO", expanded=False):
        st.json(st.session_state.log_auditoria_completo[-20:])
        if st.button("LIMPAR APENAS DADOS DE AUDITORIA"):
            st.session_state.auditoria_freios = {"exaustao": 0, "degradacao": 0, "eficiencia": 0, "fase_macro": 0}
            st.session_state.auditoria_sinais = {"CHANCE ELITE": 0, "ROSA ELITE": 0, "OBSERVANDO": 0, "AGUARDAR": 0, "OUTROS": 0}
            st.session_state.auditoria_assertividade = {"CHANCE ELITE": {"wins": 0, "loss": 0}, "ROSA ELITE": {"wins": 0, "loss": 0}, "OBSERVANDO": {"wins": 0, "loss": 0}, "AGUARDAR": {"wins": 0, "loss": 0}}
            st.session_state.log_auditoria_completo = []
            salvar_memoria()
            st.rerun()

st.markdown('<div class="main-card"><h3>🧠 STATUS DA BANCA MULTICÉREBRO</h3></div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**🛡️ Cérebro Defensivo (Fase Macro):** {fase_macro}")
    st.markdown(f"**⚡ Radar Rosa (Micro Pressão Suavizada):** {radar_score}%")
    st.markdown(f"**📉 Winrate Histórico do Padrão:** {winrate_padrao:.1f}%")
    st.markdown(f"**📉 Taxa Roxa Global:** {tx_roxa:.1f}%")
    st.markdown(f"**🔥 Taxa Roxa Quente (Contexto 50 Velas):** {tx_roxa_quente_ctx:.1f}%")
    st.markdown(f"**⚡ Densidade Roxa (Últimas 15 rds):** {densidade_roxa_v}/15")
with col2:
    st.markdown(f"**🌸 Cérebro de Expansão (Alvo Rosa):** {expansion_score}%")
    st.markdown(f"**🧬 Força Base (Core Adaptive):** {adaptive_score}%")
    st.markdown(f"**🥀 Winrate Recent do Padrão (Degradação):** {winrate_recente_padrao:.1f}%")
    st.markdown(f"**⏱️ Distância da Última Rosa:** {st.session_state.distancia_rosa} rds")

if len(st.session_state.historico) > 0:
    st.markdown('<div class="main-card"><h3>📊 MONITOR DE FLUXO EM TEMPO REAL</h3></div>', unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:18px;color:#00ff66;line-height:1.6;'>{' → '.join([f'**[{v}]**' for v in st.session_state.historico[-16:]])}</p>", unsafe_allow_html=True)

total = st.session_state.acertos + st.session_state.erros
assertividade = (st.session_state.acertos / total) * 100 if total > 0 else 0
st.markdown('<div class="gold-card"><h3 style="text-align:center;">📊 ENGINE DE VALIDAÇÃO QUANTITATIVA AVANÇADA</h3></div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: 
    st.metric("✅ ACERTOS MASTER", st.session_state.acertos)
    st.metric("📈 DRAWDOWN HISTÓRICO", f"{st.session_state.max_drawdown_calc*100:.2f}%")
    st.metric("📊 SCORE MÉDIO SINAIS", f"{st.session_state.score_medio}%")
with c2: 
    st.metric("❌ ERROS MASTER", st.session_state.erros)
    st.metric("💀 MÁXIMA SEQUÊNCIA LOSS", st.session_state.max_loss_streak)
    st.metric("🎯 TOTAL OPERAÇÕES EMITIDAS", st.session_state.total_operacoes)
with c3: 
    st.metric("📊 TAXA ACERTO GLOBAL", f"{assertividade:.1f}%")
    st.metric("🛡️ RISCO DE RUÍNA", risco_ruina_status)

if st.session_state.padroes_db:
    with st.expander("📚 FILTRAGEM INTELIGENTE - BANCO DE PADRÕES ATIVOS (PERSISTENTE)", expanded=False):
        for pad, stats in st.session_state.padroes_db.items():
            st.markdown(f"🔹 **Padrão:** `{pad}` | 🟢 Wins: **{stats['wins']}** | 🔴 Loss: **{stats['loss']}** | 📊 Winrate: **{stats['ultimo_winrate']}%**")

if st.button("RESETAR ECOSSISTEMA TOTAL"):
    if os.path.exists(ARQUIVO_MEMORIA): os.remove(ARQUIVO_MEMORIA)
    st.session_state.historico, st.session_state.banco_padroes, st.session_state.distancia_rosa, st.session_state.acertos, st.session_state.erros, st.session_state.ultimos_resultados, st.session_state.quarentena, st.session_state.memoria_positiva, st.session_state.memoria_negativa = [], [], 0, 0, 0, [], {}, [], {}
    st.session_state.perdas_consecutivas, st.session_state.max_loss_streak, st.session_state.modo_defensivo, st.session_state.cooldown_rodadas, st.session_state.sinais_ignorados, st.session_state.max_drawdown_calc, st.session_state.padroes_db, st.session_state.bloco_validacao, st.session_state.score_medio, st.session_state.total_operacoes = 0, 0, False, 0, 0, 0.0, {}, "NENHUM", 0, 0
    st.session_state.auditoria_freios = {"exaustao": 0, "degradacao": 0, "eficiencia": 0, "fase_macro": 0}
    st.session_state.auditoria_sinais = {"CHANCE ELITE": 0, "ROSA ELITE": 0, "OBSERVANDO": 0, "AGUARDAR": 0, "OUTROS": 0}
    st.session_state.auditoria_assertividade = {"CHANCE ELITE": {"wins": 0, "loss": 0}, "ROSA ELITE": {"wins": 0, "loss": 0}, "OBSERVANDO": {"wins": 0, "loss": 0}, "AGUARDAR": {"wins": 0, "loss": 0}}
    st.session_state.log_auditoria_completo = []
    st.session_state.ultima_entrada = None
    st.session_state.ultimo_contexto = None
    salvar_memoria()
    st.rerun()
