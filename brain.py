# brain.py
# =========================================================
# SNIPER OURO IA ADAPTIVE - NÚCLEO INTELIGENTE ISOLADO
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
    
    if taxa_roxa >= 70: score += 15
    if taxa_roxa >= 80: score += 20
    if taxa_roxa >= 90: score += 25
    if taxa_rosa >= 20: score += 15

    if ocorrencias >= 10: score += 10
    if ocorrencias >= 20: score += 15
    if ocorrencias >= 30: score += 20

    score += pressao_radar * 0.4

    if fase == "DEFENSIVA": score -= 15
    if len(ultimos_resultados) >= 3:
        erros = ultimos_resultados[-3:].count("LOSS")
        if erros >= 2: score -= 12
        
    return min(max(int(score), 0), 100)
