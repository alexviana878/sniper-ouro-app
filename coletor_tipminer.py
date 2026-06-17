# coletor_tipminer.py
# ==================================================
# TESTE DE CAPTURA TIPMINER
# ==================================================

import requests
from bs4 import BeautifulSoup
import re

URL = "https://tipminer.com/br/historico/betou/aviator"

def capturar_rodadas():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        # --- 🔍 RASTREAMENTO INTERNO DE EXECUÇÃO ---
        print("ANTES REQUEST")

        resposta = requests.get(
            URL,
            headers=headers,
            timeout=5
        )

        print("DEPOIS REQUEST")

        # --- 📊 PRINTS DE DIAGNÓSTICO AVANÇADO ---
        print("STATUS:", resposta.status_code)
        print("TAMANHO HTML:", len(resposta.text))
        
        # 🔬 EXPLORAÇÃO DE REDIRECIONAMENTO E METADADOS
        print("URL FINAL:")
        print(resposta.url)

        print("HEADERS:")
        print(resposta.headers)

        # 🚨 RETORNO TEMPORÁRIO DE DIAGNÓSTICO:
        # Devolve a URL final em formato de lista isolada para renderizar na tela do Sniper
        return [resposta.url]

        html = resposta.text

        # --- REGEX SEM O "x" ---
        encontrados = re.findall(
            r'(\d+,\d+)',
            html
        )

        print("PRIMEIROS 100:")
        print(encontrados[:100])

        rodadas = []

        for valor in encontrados:
            try:
                rodadas.append(
                    float(
                        valor.replace(",", ".")
                    )
                )
            except:
                pass

        return rodadas

    except Exception as erro:
        print("ERRO INTERNO NO COLETOR:", erro)
        return []


if __name__ == "__main__":
    rodadas = capturar_rodadas()

    print()
    print("TOTAL CAPTURADAS:", len(rodadas))
    print()

    print(rodadas[:50])
