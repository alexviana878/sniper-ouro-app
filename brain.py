# brain.py
# =========================================================
# ENGINE QUANTITATIVA MODULAR - MASTER PREMIUM v10.5.1
# STATUS: INDENTATION FIX & LOGIC FROZEN FOR VALIDATION
# =========================================================

def classificar_vela(valor):
    if valor < 1.20: return "X"
    elif valor < 2.00: return "B"
    elif valor < 5.00: return "R"
    elif valor < 10.00: return "P"
    elif valor < 20.00: return "A"
    return "E"

def gerar_padrao(historico):
    if len(historico) < 5: return None
    return "-".join([classificar_vela(v) for v in historico[-5:]])

def detectar_fase(historico):
    janela = historico[-20:] if len(historico) >= 20 else historico
    reds = sum(1 for x in janela if x < 2)
    altos = sum(1 for x in janela if x >= 10)
    if reds >= 12: return "DEFENSIVA"
    if altos >= 4: return "AGRESSIVA"
    return "NEUTRA"

def calcular_pressao_radar(historico, janela_ativa=False):
    janela = historico[-10:] if len(historico) >= 10 else historico
    pressao = 0
    reds = sum(1 for x in janela if x < 2)
    baixos = sum(1 for x in janela if x < 1.5)
    if reds >= 7: pressao += 35
    elif reds >= 5: pressao += 25
    elif reds >= 3: pressao += 15
    if baixos >= 5: pressao += 25
    elif baixos >= 3: pressao += 15
    if janela_ativa: pressao += 15
    return min(pressao, 100)

def calcular_compressao(historico):
    janela = historico[-15:] if len(historico) >= 15 else historico
    reds = sum(1 for x in janela if x < 2)
    medios = sum(1 for x in janela if 2 <= x < 5)
    altos = sum(1 for x in janela if x >= 10)
    score = 0
    if reds >= 8: score += 30
    if medios <= 2: score += 20
    if altos == 0: score += 40
    return min(score, 100)

def calcular_distancia_rosa(historico):
    for i in range(len(historico) - 1, -1, -1):
        if historico[i] >= 10:
            return len(historico) - i
    return 999

def detectar_expansao(historico):
    distancia = calcular_distancia_rosa(historico)
    compressao = calcular_compressao(historico)
    score = 0
    if distancia >= 10: score += 20
    if distancia >= 15: score += 35
    if distancia >= 20: score += 50
    score += compressao * 0.5
    return min(int(score), 100)

def detectar_exaustao(historico):
    if len(historico) < 6: return False
    ultimas6 = historico[-6:]
    media6 = sum(ultimas6) / 6
    altos = len([v for v in ultimas6 if v >= 5])
    rosas = len([v for v in ultimas6 if v >= 10])
    baixos = len([v for v in ultimas6 if v <= 1.30])
    if media6 >= 3.8: return True
    if altos >= 3: return True
    if rosas >= 2: return True
    if baixos >= 5: return True
    return False

def detectar_aceleracao(historico):
    if len(historico) < 8:
        return {"roxa": False, "rosa": False, "densidade": False}
    ultimas8 = historico[-8:]
    ultimas4 = historico[-4:]
    media8 = sum(ultimas8) / 8
    media4 = sum(ultimas4) / 4
    roxas8 = len([v for v in ultimas8 if v >= 2])
    roxas4 = len([v for v in ultimas4 if v >= 2])
    rosas4 = len([v for v in ultimas4 if v >= 10])
    aceleracao_roxa = (roxas4 >= 2 and roxas8 >= 3 and media4 > media8)
    aceleracao_rosa = (rosas4 >= 1 and media4 >= 4)
    aceleracao_densidade = (media8 <= 1.7 and media4 >= 2.4)
    return {"roxa": aceleracao_roxa, "rosa": aceleracao_rosa, "densidade": aceleracao_densidade}

def calcular_eficiencia_recente(ultimos_resultados):
    if not ultimos_resultados: return 0.0
    janela = ultimos_resultados[-20:]
    wins = janela.count("WIN")
    return wins / len(janela)

class RiskManager:
    def __init__(self):
        self.loss_streak = 0
        self.max_loss_streak = 0
        self.pause_mode = False
        self.cooldown_rodadas = 0
        self.saldo_virtual = 1000.0
        self.topo_saldo = 1000.0
        self.drawdown = 0.0

    def calcular_risco_ruina(self, acertos, erros, max_loss):
        total = acertos + erros
        if total < 10 or max_loss == 0: 
            return "BAIXO (COLETANDO DATA)"
        winrate = acertos / total
        if winrate >= 0.60 and max_loss <= 3: return "💎 SEGURO (MÍNIMO)"
        elif winrate >= 0.50 and max_loss <= 5: return "🟡 MODERADO (MÉDIO)"
        elif winrate < 0.45 or max_loss >= 6: return "🚨 ALTO (RISCO DE QUEBRA)"
        return "NEUTRO"

def calcular_score_adaptive(historico, taxa_roxa, tx_roxa_quente_ctx, ocorrencias, winrate_padrao, winrate_recente_padrao, ultimos_resultados, janela_ativa=False):
    score = 0
    fase = detectar_fase(historico)
    pressao_radar = calcular_pressao_radar(historico, janela_ativa)
    eficiencia_recente = calcular_eficiencia_recente(ultimos_resultados)

    if len(historico) >= 10:
        reds_curto_5 = sum(1 for x in historico[-5:] if x < 2)
        reds_medio_7 = sum(1 for x in historico[-7:] if x < 2)
        reds_longo_10 = sum(1 for x in historico[-10:] if x < 2)
        if reds_curto_5 >= 4: score += 10
        if reds_medio_7 >= 5: score += 10
        if reds_longo_10 >= 8: score += 15

    if tx_roxa_quente_ctx >= 60: score += 25
    elif tx_roxa_quente_ctx >= 50: score += 20
    elif tx_roxa_quente_ctx >= 40: score += 15

    if taxa_roxa >= 90: score += 15
    elif taxa_roxa >= 80: score += 10

    if ocorrencias >= 30 and winrate_padrao >= 55.0: score += 20
    elif ocorrencias >= 20 and winrate_padrao >= 50.0: score += 15
    elif ocorrencias >= 10 and winrate_padrao >= 45.0: score += 10

    ultimas15 = historico[-15:] if len(historico) >= 15 else historico
    densidade_roxa = sum(1 for x in ultimas15 if x >= 2)
    if densidade_roxa >= 9: score += 25
    elif densidade_roxa <= 4: score -= 20

    if densidade_roxa >= 8 and taxa_roxa >= 45.0 and pressao_radar >= 65:
        score += 15

    score += pressao_radar * 0.35
    if fase == "DEFENSIVA": score -= 15

    if eficiencia_recente >= 0.70: score += 15
    elif eficiencia_recente <= 0.45: score -= 20

    if winrate_recente_padrao < 45.0 and ocorrencias >= 5: score -= 25
    if detectar_exaustao(historico): score -= 20

    return min(max(int(score), 0), 100)

def calcular_consenso(adaptive_score, radar_score, expansion_score, fase_macro, tx_roxa_quente_ctx, mercado_instavel, historico, winrate_padrao, winrate_recente_padrao):
    if detectar_exaustao(historico): return "🛑 EXAUSTÃO DELTA", 0
    if mercado_instavel: return "⚠️ MERCADO INSTÁVEL", 0

    if winrate_padrao >= 50.0 and winrate_recente_padrao <= 25.0:
        return "⚠️ DEGRADAÇÃO ACELERADA", 0

    peso_adaptive = 0.50
    peso_radar = 0.30
    peso_expansion = 0.20

    if expansion_score >= 75:
        peso_expansion = 0.30
        peso_adaptive = 0.40
    if radar_score >= 80:
        peso_radar = 0.40
        peso_adaptive = 0.40

    score_final = (adaptive_score * peso_adaptive) + (radar_score * peso_radar) + (expansion_score * peso_expansion)

    if tx_roxa_quente_ctx < 38.0 and radar_score < 45: return "⚠️ PRESSÃO FRACA", int(score_final)
    if expansion_score >= 88 and adaptive_score >= 78 and tx_roxa_quente_ctx >= 55: return "🌸 ROSA ELITE", int(score_final)
    if adaptive_score >= 68 and radar_score >= 58 and tx_roxa_quente_ctx >= 48: return "🟢 CHANCE ELITE", int(score_final
