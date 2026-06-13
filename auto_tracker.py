# auto_tracker.py
# ====================================================================
# SCRIPT DE RASTREAMENTO AUTOMÁTICO E AUDITORIA DE SINAIS (SQLITE)
# VERSÃO: 1.9.5 - INTEGRAÇÃO INTEGRAL DE SINAL COGNITIVO PREMIUM
# ====================================================================

import sqlite3
import os
from datetime import datetime

# --- CONFIGURAÇÃO MASTER DO LABORATÓRIO ---
JANELA_MAXIMA = 5  

# Definição do caminho do banco de dados local na mesma pasta do script
DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tracker.db")

def inicializar_banco():
    """Cria o banco de dados, as tabelas e os índices de alta performance para milhares de registros."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Criação da tabela de sinais
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sinais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        timestamp_resultado TEXT DEFAULT NULL,
        tipo TEXT NOT NULL,
        adaptive INTEGER NOT NULL,
        radar INTEGER NOT NULL,
        expansion INTEGER NOT NULL,
        tx_quente REAL NOT NULL,
        padrao TEXT NOT NULL,
        rodada_origem INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'PENDENTE',
        resultado REAL DEFAULT NULL,
        delay_rodadas INTEGER DEFAULT 0,
        consenso REAL DEFAULT 0.0,
        resultado_categoria TEXT DEFAULT NULL,
        fase_macro TEXT DEFAULT 'NEUTRA'
    )
    """)
    
    # --- 🛡️ ETAPA 1 ROBUSTA: TABELA INSIGHTS TIPMINER COM CONSTRAINT UNIQUE ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insights_tipminer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contexto TEXT UNIQUE,
        total_amostras INTEGER,
        wins INTEGER,
        losses INTEGER,
        winrate REAL,
        consenso_medio REAL,
        delay_medio REAL,
        ultima_atualizacao TEXT
    )
    """)
    
    # --- ⚡ ACELERAÇÃO FUTURA: CRIAÇÃO DE ÍNDICES QUANT MASTER ---
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sinais_status ON sinais(status);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sinais_consenso ON sinais(consenso);")
    
    # --- 🛡️ ENGINE MASTER DE MIGRAÇÃO AUTOMÁTICA DE COLUNAS ---
    cursor.execute("PRAGMA table_info(sinais)")
    colunas_existentes = [col[1] for col in cursor.fetchall()]
    
    if "delay_rodadas" not in colunas_existentes:
        cursor.execute("ALTER TABLE sinais ADD COLUMN delay_rodadas INTEGER DEFAULT 0")
    if "consenso" not in colunas_existentes:
        cursor.execute("ALTER TABLE sinais ADD COLUMN consenso REAL DEFAULT 0.0")
    if "timestamp_resultado" not in colunas_existentes:
        cursor.execute("ALTER TABLE sinais ADD COLUMN timestamp_resultado TEXT DEFAULT NULL")
    if "resultado_categoria" not in colunas_existentes:
        cursor.execute("ALTER TABLE sinais ADD COLUMN resultado_categoria TEXT DEFAULT NULL")
    if "fase_macro" not in colunas_existentes:
        cursor.execute("ALTER TABLE sinais ADD COLUMN fase_macro TEXT DEFAULT 'NEUTRA'")
        
    conn.commit()
    conn.close()

def registrar_sinal(tipo, adaptive_score, radar_score, expansion_score, tx_roxa_quente, padrao, rodada, consenso, fase_macro):
    """Registra um sinal emitido pelo cérebro armazenando as métricas e a fase macro do mercado."""
    inicializar_banco()
    
    # --- 🛡️ HIERARQUIA ATUALIZADA COM ENTRADA PREMIUM ---
    sinais_validos = [
        "🟠 PRÉ ELITE", "🟢 CHANCE ELITE", "🌸 ROSA ELITE", "💎 PREMIUM", "🟡 OBSERVANDO",
        "PRÉ ELITE", "CHANCE ELITE", "ROSA ELITE", "PREMIUM", "OBSERVANDO",
        "PRE_ELITE", "CHANCE_ELITE", "ROSA_ELITE", "PREMIUM"
    ]
    
    tipo_limpo = (
        tipo.replace("🟠 ", "")
            .replace("🟢 ", "")
            .replace("🌸 ", "")
            .replace("💎 ", "")
            .replace("🟡 ", "")
            .strip()
    )
    
    if tipo in sinais_validos or tipo_limpo in ["PRÉ ELITE", "CHANCE ELITE", "ROSA ELITE", "PREMIUM", "OBSERVANDO"]:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        timestamp_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
        INSERT INTO sinais (timestamp, tipo, adaptive, radar, expansion, tx_quente, padrao, rodada_origem, status, delay_rodadas, consenso, fase_macro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'PENDENTE', 0, ?, ?)
        """, (timestamp_atual, tipo_limpo, int(adaptive_score), int(radar_score), int(expansion_score), float(tx_roxa_quente), str(padrao), int(rodada), float(consenso), str(fase_macro)))
        
        conn.commit()
        conn.close()

def atualizar_resultado(vela_final, rodada_atual):
    """Varre todos os sinais PENDENTES no banco de dados de forma simultânea."""
    inicializar_banco()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, tipo, rodada_origem FROM sinais WHERE status = 'PENDENTE'
    """)
    sinais_pendentes = cursor.fetchall()
    
    vela_final = float(vela_final)
    rodada_atual = int(rodada_atual)
    timestamp_fechamento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for row in sinais_pendentes:
        sinal_id, tipo_sinal, rodada_origem = row
        delay_calculado = rodada_atual - rodada_origem
        
        alvo_minimo = 10.0 if "ROSA" in tipo_sinal else 2.0
        deu_green = vela_final >= alvo_minimo
        
        if vela_final >= 10.0:
            categoria_vela = "GREEN_ROSA"
        elif vela_final >= 5.0:
            categoria_vela = "GREEN_5X"
        elif vela_final >= 2.0:
            categoria_vela = "GREEN_2X"
        else:
            categoria_vela = "LOSS"
            
        if deu_green:
            cursor.execute("""
            UPDATE sinais 
            SET status = 'WIN', resultado = ?, delay_rodadas = ?, timestamp_resultado = ?, resultado_categoria = ? 
            WHERE id = ?
            """, (vela_final, delay_calculado, timestamp_fechamento, categoria_vela, sinal_id))
        else:
            if delay_calculado >= JANELA_MAXIMA:
                cursor.execute("""
                UPDATE sinais 
                SET status = 'LOSS', resultado = ?, delay_rodadas = ?, timestamp_resultado = ?, resultado_categoria = 'LOSS' 
                WHERE id = ?
                """, (vela_final, delay_calculado, timestamp_fechamento, sinal_id))
            else:
                pass
                
    conn.commit()
    conn.close()

def obter_metricas_painel():
    """Retorna volumetria completa, taxas de acerto, atrasos, consensos e quebras de categorias."""
    inicializar_banco()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # --- 📊 FUNIL ATUALIZADO PARA O PAINEL GERAL ---
    tipos = ["ROSA ELITE", "CHANCE ELITE", "PREMIUM", "PRÉ ELITE", "OBSERVANDO"]
    metricas = {}
    
    for t in tipos:
        cursor.execute("SELECT COUNT(*) FROM sinais WHERE tipo = ? AND status = 'WIN'", (t,))
        wins = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sinais WHERE tipo = ? AND status = 'LOSS'", (t,))
        losses = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sinais WHERE tipo = ?", (t,))
        total_registrado = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(delay_rodadas) FROM sinais WHERE tipo = ? AND status = 'WIN'", (t,))
        avg_delay = cursor.fetchone()[0]
        avg_delay = round(avg_delay, 1) if avg_delay is not None else 0.0
        
        cursor.execute("SELECT AVG(consenso) FROM sinais WHERE tipo = ?", (t,))
        avg_consenso = cursor.fetchone()[0]
        avg_consenso = round(avg_consenso, 1) if avg_consenso is not None else 0.0
        
        cursor.execute("SELECT COUNT(*) FROM sinais WHERE tipo = ? AND resultado_categoria = 'GREEN_2X'", (t,))
        g2x = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sinais WHERE tipo = ? AND resultado_categoria = 'GREEN_5X'", (t,))
        g5x = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sinais WHERE tipo = ? AND resultado_categoria = 'GREEN_ROSA'", (t,))
        g_rosa = cursor.fetchone()[0]
        
        total_resolvidos = wins + losses
        winrate = round((wins / total_resolvidos) * 100, 1) if total_resolvidos > 0 else 0.0
        
        metricas[t] = {
            "wins": wins,
            "losses": losses,
            "total_resolvidos": total_resolvidos,
            "registrados": total_registrado,
            "pendentes": total_registrado - total_resolvidos,
            "winrate": winrate,
            "avg_delay": avg_delay,
            "avg_consenso": avg_consenso,
            "vol_2x": g2x,
            "vol_5x": g5x,
            "vol_rosa": g_rosa
        }
        
    conn.close()
    return metricas

inicializar_banco()
