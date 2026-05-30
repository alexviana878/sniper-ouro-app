# brain.py
# =========================================================
# ENGINE QUANTITATIVA MODULAR - MASTER PREMIUM v10.5
# RECURSOS: TAXA QUENTE CONTEXTUAL, RADAR GRADUAL & CONVERGÊNCIA DELTA
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

# =========================================================
# ⚙️ PRIORIDADE 4: RADAR ROSA GRADUAL (Suavizado para evitar saturação rápida em 100%)
# =========================================================
def calcular_pressao_radar(historico, janela_ativa=False):
    janela = historico[-10:] if len(historico) >= 10 else historico
    pressao = 0
    reds = sum(1 for x in janela if x < 2)
    baixos = sum(1 for x in janela if x < 1.5)

    # Escala de pontuação gradual para gerar meio-termo real (24%, 45%, 70%...)
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
    altos = sum(1 for x in filename_or_history if x >= 10) if 'filename_or_history' in locals() else sum(1 for x in janela if x >= 10)
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

    return {
        "roxa": aceleracao_roxa,
        "rosa": aceleracao_rosa,
        "densidade": aceleracao_densidade
    }

def calcular_eficiencia_recente(ultimos_resultados):
    if not ultimos_resultados: return 0.0
    janela = ultimos_resultados[-20:]
    wins = janela.count("WIN")
    return wins / len(janela)

# =========================================================
# MÓDULO RISK ENGINE
# =========================================================
class RiskManager:
    def __init__(self):
