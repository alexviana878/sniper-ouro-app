import numpy as np

def gerar_padrao(historico_velas):
    """Gera o padrão visual dos últimos 5 resultados (ex: B-B-R-B-X)"""
    if len(historico_velas) < 5:
        return "---"
    ultimas = historico_velas[-5:]
    mapeado = []
    for v in ultimas:
        if v >= 10.0:
            mapeado.append("X") # Rosa/Super Vela
        elif v >= 2.0:
            mapeado.append("R") # Roxa
        else:
            mapeado.append("B") # Branca
    return "-".join(mapeado)

def detectar_fase(historico_velas):
    """Cérebro Defensivo: Avalia a saúde do mercado nas últimas 30 rodadas"""
    if len(historico_velas) < 30:
        return "NEUTRA"
    amostra = historico_velas[-30:]
    roxas = sum(1 for x in amostra if x >= 2.0)
    taxa = (roxas / 30) * 100
    
    if taxa >= 55:
        return "ALTA EXPLOSÃO"
    elif taxa >= 40:
        return "ESTÁVEL"
    elif taxa >= 28:
        return "NEUTRA"
    else:
        return "RECOVERY (URGENTE)"

def calcular_pressao_radar(historico_velas, janela_ativa=False):
    """Radar Rosa: Mede a micro pressão de subida para buscar velas pagantes"""
    if len(historico_velas) < 15:
        return 50
    ultimas = historico_velas[-15:]
    brancas_seguidas = 0
    for v in reversed(ultimas):
        if v < 2.0:
            brancas_seguidas += 1
        else:
            break
            
    base_pressao = 40 + (brancas_seguidas * 7)
    if janela_ativa:
        base_pressao += 12
        
    return min(max(base_pressao, 0), 100)

def detectar_expansao(historico_velas):
    """Cérebro de Expansão: Alvo para buscar a vela Rosa de proteção/alavancagem"""
    if len(historico_velas) < 20:
        return 50
    ultimas = historico_velas[-20:]
    rosas = sum(1 for x in ultimas if x >= 10.0)
    
    if rosas == 0:
        return 75  # Saturação de falta de Rosa (está prestes a sair)
    elif rosas == 1:
        return 55
    else:
        return 35  # Mercado já distribuiu muitas rosas recentemente

def detectar_aceleracao(historico_velas):
    """Mapeia acelerações rápidas de momento"""
    if len(historico_velas) < 3:
        return {"roxa": False, "rosa": False}
    ultimas = historico_velas[-3:]
    
    # Se as duas últimas subiram progressivamente
    acelerando = ultimas[-1] > ultimas[-2] > ultimas[-3]
    return {
        "roxa": acelerando and ultimas[-1] >= 2.0,
        "rosa": acelerando and ultimas[-1] >= 5.0
    }

def calcular_score_adaptive(historico, tx_roxa, tx_roxa_quente_ctx, ocorrencias, winrate_padrao, winrate_recente_padrao, ultimos_resultados, janela_ativa):
    """
    Core Adaptive: Calcula a pontuação do padrão cruzando histórico e degradação.
    Retorna o score final e o dicionário completo estruturado para a auditoria automática.
    """
    # 1. Definição do Score Base estrutural com base na força estatística do padrão
    if ocorrencias > 8:
        score_base = int(winrate_padrao)
    else:
        score_base = 50 # Neutro por falta de amostragem robusta

    # Inicialização das penalidades (freios internos)
    penalidade_exaustao = 0
    penalidade_degradacao = 0
    penalidade_eficiencia = 0
    penalidade_fase = 0

    # 2. Aplicação do Freio 1: Exaustão (Mercado esticado demais no curto prazo)
    if tx_roxa_quente_ctx > 60:
        penalidade_exaustao = 15

    # 3. Aplicação do Freio 2: Degradação Recente (Padrão começou a errar nas últimas vezes)
    if winrate_recente_padrao < 45:
        penalidade_degradacao = 20
    elif winrate_recente_padrao < winrate_padrao - 15:
        penalidade_degradacao = 10

    # 4. Aplicação do Freio 3: Eficiência Global da Sessão
    if len(ultimos_resultados) >= 6:
        ultimos_seis = ultimos_resultados[-6:]
        if ultimos_seis.count("LOSS") >= 4:
            penalidade_eficiencia = 15

    # 5. Aplicação do Freio 4: Cérebro Defensivo (Fase Macro de perigo)
    fase = detectar_fase(historico)
    if fase == "RECOVERY (URGENTE)":
        penalidade_fase = 25
    elif fase == "NEUTRA":
        penalidade_fase = 5

    # 6. Montagem do dicionário de auditoria com chaves estritas (Evita KeyError no Streamlit)
    auditoria_dict = {
        "score_base": score_base,
        "penalidade_exaustao": penalidade_exaustao,
        "penalidade_degradacao": penalidade_degradacao,
        "penalidade_eficiencia": penalidade_eficiencia,
        "penalidade_fase": penalidade_fase
    }

    # Cálculo final do Core de forma matemática e limpa
    score_final = score_base - (penalidade_exaustao + penalidade_degradacao + penalidade_eficiencia + penalidade_fase)
    score_final = max(min(score_final, 100), 0)

    return score_final, auditoria_dict

def calcular_consenso(adaptive_score, radar_score, expansion_score, fase_macro, tx_roxa_quente_ctx, mercado_instavel, historico, winrate_padrao, winrate_recente_padrao):
    """Gera o veredito final com base no cruzamento de todos os cérebros do ecossistema"""
    
    # Média ponderada dos motores de análise
    media_consenso = int((adaptive_score * 0.5) + (radar_score * 0.3) + (expansion_score * 0.2))
    
    # Filtros de segurança macro
    if fase_macro == "RECOVERY (URGENTE)" or mercado_instavel:
        return "AGUARDAR", media_consenso
        
    # Critérios estritos para emissão de Sinais Master
    if media_consenso >= 78 and winrate_recente_padrao >= 60:
        if expansion_score >= 70 and radar_score >= 65:
            return "🌸 ROSA ELITE", media_consenso
        return "🎯 CHANCE ELITE", media_consenso
    elif media_consenso >= 55:
        return "👀 OBSERVANDO", media_consenso
    else:
        return "⚠️ AGUARDAR", media_consenso

class RiskManager:
    """Gerenciador de Risco Avançado para proteção patrimonial da banca"""
    def __init__(self):
        pass

    def calcular_risco_ruina(self, acertos, erros, max_loss_streak):
        total = acertos + erros
        if total < 10:
            return "ANALISANDO..."
        
        winrate = (acertos / total) * 100
        if max_loss_streak >= 5 or winrate < 40:
            return "🔴 ALTO PERIGO"
        elif max_loss_streak >= 3 or winrate < 50:
            return "🟡 MODERADO"
        else:
            return "🟢 SEGURO"
