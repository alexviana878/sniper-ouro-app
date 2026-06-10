# auto_tracker.py
# ====================================================================
# SCRIPT DE RASTREAMENTO AUTOMÁTICO E AUDITORIA DE SINAIS (SQLITE)
# VERSÃO: 1.7.0 - RELATÓRIO COMPLETO COM MÉTRICAS DE SINAIS PENDENTES
# ====================================================================

import sqlite3
import os
from datetime import datetime

# --- CONFIGURAÇÃO MASTER DO LABORATÓRIO ---
# Janela máxima configurável para evitar matar sinais que maturam mais tarde
JANELA_MAXIMA = 5  

# Definição do caminho do banco de dados local na mesma pasta do script
DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tracker.db")

def inicializar_banco():
    """Cria o banco de dados e a tabela de sinais, aplicando migrações de colunas na risca."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Criação da tabela com suporte total às melhorias do laboratório
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
    """
    Registra um sinal emitido pelo cérebro armazenando as métricas e a fase macro do mercado.
    Aceita: ROSA ELITE, CHANCE ELITE, PRÉ ELITE e OBSERVANDO.
    """
    inicializar_banco()
    
    sinais_validos = [
        "🟠 PRÉ ELITE", "🟢 CHANCE ELITE", "🌸 ROSA ELITE", "🟡 OBSERVANDO",
        "PRÉ ELITE", "CHANCE ELITE", "ROSA ELITE", "OBSERVANDO",
        "PRE_ELITE", "CHANCE_ELITE", "ROSA_ELITE"
    ]
    
    tipo_limpo = (
        tipo.replace("🟠 ", "")
            .replace("🟢 ", "")
            .replace("🌸 ", "")
            .replace("🟡 ", "")
            .strip()
    )
    
    if tipo in sinais_validos or tipo_limpo in ["PRÉ ELITE", "CHANCE ELITE", "ROSA ELITE", "OBSERVANDO"]:
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
    """
    Varre todos os sinais PENDENTES no banco de dados de forma simultânea.
    Aplica alvos matemáticos independentes e respeita a JANELA_MAXIMA de maturação configurável.
    """
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
        
        # Definição de alvo mínimo de sobrevivência do sinal
        alvo_minimo = 10.0 if "ROSA" in tipo_sinal else 2.0
        deu_green = vela_final >= alvo_minimo
        
        # Lógica de Mapeamento e Categorização da força da vela obtida
        if vela_final >= 10.0:
            categoria_vela = "GREEN_ROSA"
        elif vela_final >= 5.0:
            categoria_vela = "GREEN_5X"
        elif vela_final >= 2.0:
            categoria_vela = "GREEN_2X"
        else:
            categoria_vela = "LOSS"
            
        if deu_green:
            # Sinal bateu o alvo esperado dentro do prazo de tolerância!
            cursor.execute("""
            UPDATE sinais 
            SET status = 'WIN', resultado = ?, delay_rodadas = ?, timestamp_resultado = ?, resultado_categoria = ? 
            WHERE id = ?
            """, (vela_final, delay_calculado, timestamp_fechamento, categoria_vela, sinal_id))
        else:
            # Se não bateu o alvo mínimo e estourou a janela máxima configurável, decreta LOSS
            if delay_calculado >= JANELA_MAXIMA:
                cursor.execute("""
                UPDATE sinais 
                SET status = 'LOSS', resultado = ?, delay_rodadas = ?, timestamp_resultado = ?, resultado_categoria = 'LOSS' 
                WHERE id = ?
                """, (vela_final, delay_calculado, timestamp_fechamento, sinal_id))
            else:
                # O sinal mantém status PENDENTE para colher o desfecho nas próximas velas da janela
                pass
                
    conn.commit()
    conn.close()

def obter_metricas_painel():
    """Retorna volumetria completa, taxas de acerto, atrasos, consensos e quebras de categorias."""
    inicializar_banco()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    tipos = ["CHANCE ELITE", "ROSA ELITE", "PRÉ ELITE", "OBSERVANDO"]
    metricas = {}
    
    for t in tipos:
        cursor.execute("SELECT COUNT(*) FROM sinais WHERE tipo = ? AND status = 'WIN'", (t,))
        wins = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sinais WHERE tipo = ? AND status = 'LOSS'", (t,))
        losses = cursor.fetchone()[0]
        
        # Puxa o volume bruto histórico total absoluto emitido para este sinal
        cursor.execute("SELECT COUNT(*) FROM sinais WHERE tipo = ?", (t,))
        total_registrado = cursor.fetchone()[0]
        
        # Média de delays apenas das operações vitoriosas
        cursor.execute("SELECT AVG(delay_rodadas) FROM sinais WHERE tipo = ? AND status = 'WIN'", (t,))
        avg_delay = cursor.fetchone()[0]
        avg_delay = round(avg_delay, 1) if avg_delay is not None else 0.0
        
        # Extração da média do Consenso Master real enviado
        cursor.execute("SELECT AVG(consenso) FROM sinais WHERE tipo = ?", (t,))
        avg_consenso = cursor.fetchone()[0]
        avg_consenso = round(avg_consenso, 1) if avg_consenso is not None else 0.0
        
        # Extração de estatísticas de categorias de velas
        cursor.execute("SELECT COUNT(*) FROM sinais WHERE tipo = ? AND resultado_categoria = 'GREEN_2X'", (t,))
        g2x = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sinais WHERE tipo = ? AND resultado_categoria = 'GREEN_5X'", (t,))
        g5x = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sinais WHERE tipo = ? AND resultado_categoria = 'GREEN_ROSA'", (t,))
        g_rosa = cursor.fetchone()[0]
        
        total_resolvidos = wins + losses
        winrate = round((wins / total_resolvidos) * 100, 1) if total_resolvidos > 0 else 0.0
        
        # 🔥 ADICIONADO EXPLICITAMENTE O DICIONÁRIO COMPLETO COM O CAMPO "PENDENTES" SOLICITADO
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

# Inicialização automática de segurança estrutural
inicializar_banco()
