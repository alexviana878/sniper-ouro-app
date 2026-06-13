# tipminer.py
# ====================================================================
# MOTOR DE EXTRAÇÃO DE INSIGHTS E APRENDIZADO AUTOMÁTICO (TIPMINER V1)
# VERSÃO: 1.3.5 - ORDENAÇÃO POR RELEVÂNCIA ESTATÍSTICA (AMOSTRAGEM DESC)
# ====================================================================

import sqlite3
import os
from datetime import datetime

# Garante o apontamento correto para o tracker.db na mesma pasta raiz
DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tracker.db")

def minerar_insights():
    """
    Analisa o histórico de sinais processados, agrupa por Tipo de Sinal e faixas de 
    consenso puras, utilizando Upsert para granularizar a matriz de assertividade.
    """
    if not os.path.exists(DB_NAME):
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Query quant com o CAST para estabilização de gavetas de piso
    cursor.execute("""
    SELECT
        tipo,
        CAST(consenso / 10 AS INTEGER) * 10 as faixa_consenso,
        COUNT(*),
        SUM(CASE WHEN status='WIN' THEN 1 ELSE 0 END),
        SUM(CASE WHEN status='LOSS' THEN 1 ELSE 0 END),
        AVG(delay_rodadas),
        AVG(consenso)
    FROM sinais
    WHERE status IN ('WIN','LOSS')
    GROUP BY tipo, faixa_consenso
    """)

    resultados = cursor.fetchall()

    for row in resultados:
        tipo, faixa, total, wins, losses, delay, consenso = row

        if total == 0:
            continue

        # Formatação matemática precisa das métricas por faixa
        winrate = round((wins / total) * 100, 2)
        delay_medio = round(delay, 2) if delay is not None else 0.0
        consenso_medio = round(consenso, 2) if consenso is not None else 0.0
        
        # Engine de higienização de rótulos
        tipo_limpo = (
            str(tipo)
            .replace(" ", "_")
            .replace("🟠", "")
            .replace("🟢", "")
            .replace("🌸", "")
            .replace("💎", "")
            .replace("🟡", "")
            .strip()
        )

        contexto_label = f"{tipo_limpo}_{int(faixa)}"

        # --- 🚀 QUERY UNIFICADA: UPSERT MASTER COM ON CONFLICT(contexto) ---
        cursor.execute("""
        INSERT INTO insights_tipminer (
            contexto,
            total_amostras,
            wins,
            losses,
            winrate,
            consenso_medio,
            delay_medio,
            ultima_atualizacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(contexto) DO UPDATE SET
            total_amostras = excluded.total_amostras,
            wins = excluded.wins,
            losses = excluded.losses,
            winrate = excluded.winrate,
            consenso_medio = excluded.consenso_medio,
            delay_medio = excluded.delay_medio,
            ultima_atualizacao = excluded.ultima_atualizacao
        """,
        (
            contexto_label,
            total,
            wins,
            losses,
            winrate,
            consenso_medio,
            delay_medio,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

    conn.commit()
    conn.close()


def obter_insights():
    """
    Busca os dados gerados na tabela insights_tipminer, trata as tuplas brutas
    e converte em dicionário ordenando por peso de amostragem e taxa de vitória.
    """
    dados = {}
    if not os.path.exists(DB_NAME):
        return dados

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # --- 🛡️ ALTERAÇÃO CIRÚRGICA: ORDENAÇÃO POR AMOSTRAGEM E DEPOIS POR WINRATE ---
        cursor.execute("""
            SELECT
                contexto,
                total_amostras,
                wins,
                losses,
                winrate,
                consenso_medio,
                delay_medio,
                ultima_atualizacao
            FROM insights_tipminer
            ORDER BY total_amostras DESC, winrate DESC
        """)
        
        resultados = cursor.fetchall()
        
        for row in resultados:
            contexto = row[0]
            dados[contexto] = {
                "total": row[1],
                "wins": row[2],
                "losses": row[3],
                "winrate": row[4],
                "consenso_medio": row[5],
                "delay_medio": row[6],
                "ultima_atualizacao": row[7]
            }
    except Exception as e:
        print("ERRO INTERNO TIPMINER EXTRACTION:", e)

    conn.close()
    return dados
