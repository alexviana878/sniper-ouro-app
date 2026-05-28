# brain.py
# =========================================================
# ECOSSISTEMA PREMIUM V3: CONTEXTO COMPOSTO E AMBIENTE RUIM
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
    
    if reds >= 3: pressao += 20
    if reds >= 5: pressao += 40
    if baixos >= 3: pressao += 20
    if janela_ativa: pressao += 20
    
    return min(pressao, 100)

def calcular_score_adaptive(historico, taxa_roxa, taxa_rosa, ocorrencias, ultimos_resultados, janela_ativa=False):
    score = 0
    fase = detectar_fase(historico)
    pressao_radar = calcular_pressao_radar(historico, janela_ativa)
    
    if len(historico) >= 10:
        reds_curto_5 = sum(1 for x in historico[-5:] if x < 2)
        reds_medio_7 = sum(1 for x in historico[-7:] if x < 2)
        reds_longo_10 = sum(1 for x in historico[-10:] if x < 2)
        
        if reds_curto_5 >= 4: score += 10
        if reds_medio_7 >= 5: score += 10
        if reds_longo_10 >= 8: score += 15

    if taxa_roxa >= 70: score += 15
    if taxa_roxa >= 80: score += 20
    if taxa_roxa >= 90: score += 25
    if taxa_rosa >= 20: score += 15

    if ocorrencias >= 10: score += 10
    if ocorrencias >= 20: score += 15
    if ocorrencias >= 30: score += 20

    score += pressao_radar * 0.35

    if fase == "DEFENSIVA": score -= 15
    
    if ultimos_resultados:
        # Puxa apenas a janela móvel limitada (recente) para avaliar consistência
        janela_performance = ultimos_resultados[-10:]
        wins = janela_performance.count("WIN")
        consistencia = (wins / len(janela_performance)) * 100
        
        if consistencia >= 70: score += 15
        elif consistencia <= 30: score -= 20
        
    return min(max(int(score), 0), 100)

def calcular_distancia_rosa(historico):
    for i in range(len(historico) - 1, -1, -1):
        if historico[i] >= 10:
            return len(historico) - i
    return 999

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

def detectar_expansao(historico):
    distancia = calcular_distancia_rosa(historico)
    compressao = calcular_compressao(historico)
    
    score = 0
    if distancia >= 10: score += 20
    if distancia >= 15: score += 35
    if distancia >= 20: score += 50
    
    score += compressao * 0.5
    return min(int(score), 100)

def calcular_consenso(adaptive_score, radar_score, expansion_score, fase_macro, tx_roxa):
    # ⚠️ PRIORIDADE 5: DETECTAR AMBIENTE RUIM (Bloqueio preventivo total)
    if tx_roxa < 35 and radar_score < 40 and expansion_score < 40:
        return "🔴 AMBIENTE INSTÁVEL (🚫)", 0

    if expansion_score >= 85 and adaptive_score >= 70 and radar_score >= 70:
        final_rosa = (adaptive_score * 0.35) + (radar_score * 0.25) + (expansion_score * 0.40)
        return "🌸 POSSÍVEL ROSA ELITE", min(int(final_rosa), 100)

    peso_adaptive = 0.50
    peso_radar = 0.20
    peso_expansion = 0.30
    
    if expansion_score >= 70:
        peso_adaptive = 0.35
        peso_radar = 0.25
        peso_expansion = 0.40
        
    final = (adaptive_score * peso_adaptive) + (radar_score * peso_radar) + (expansion_score * peso_expansion)
    
    if fase_macro == "DEFENSIVA":
        final -= 20
        
    final = max(0, min(100, int(final)))
    
    if final >= 92: return "🔥 ENTRADA ELITE (2x)", final
    if final >= 82: return "🟢 BOA CHANCE AGORA (2x)", final
    if final >= 50: return "🟡 OBSERVANDO", final
    return "🔴 AGUARDAR", final
