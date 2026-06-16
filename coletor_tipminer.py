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
        
        # 🧪 INJEÇÃO DE IMPRESSÃO BRUTA AMPLIADA PARA 5000 CARACTERES NO LOG
        print("INICIO HTML:")
        print(resposta.text[:5000])

        # 🚨 RETORNO TEMPORÁRIO DE DIAGNÓSTICO ESTRUTURAL AMPLIADO:
        # Interrompe o fluxo e cospe os 5000 caracteres iniciais na tela do Sniper
        return resposta.text[:5000]

        html = resposta.text

        encontrados = re.findall(
            r'(\d+,\d+)x',
            html
        )

        # --- 🔬 DIAGNÓSTICO DO REGEX ---
        print("ENCONTRADOS BRUTOS:", len(encontrados))
        print(encontrados[:50])

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
