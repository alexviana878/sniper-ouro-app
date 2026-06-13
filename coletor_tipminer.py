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

        resposta = requests.get(
            URL,
            headers=headers,
            timeout=5
        )

        # --- 📊 PRINTS DE DIAGNÓSTICO AVANÇADO ---
        print("STATUS:", resposta.status_code)
        print("TAMANHO HTML:", len(resposta.text))

        html = resposta.text

        encontrados = re.findall(
            r'(\d+,\d+)x',
            html
        )

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
        print("ERRO:", erro)
        return []


if __name__ == "__main__":
    rodadas = capturar_rodadas()

    print()
    print("TOTAL CAPTURADAS:", len(rodadas))
    print()

    print(rodadas[:50])
