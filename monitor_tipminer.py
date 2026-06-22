from playwright.sync_api import sync_playwright

URL = "https://tipminer.com/br/historico/betou/aviator"

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        channel="chrome"
    )

    page = browser.new_page()

    page.goto(URL)

    print("TIPMINER ABERTO")

    input("FAÇA LOGIN E APERTE ENTER")

    print("PÁGINA CARREGADA")

    texto = page.locator("body").inner_text()

    print()
    print("PRIMEIROS 3000 CARACTERES:")
    print()
    print(texto[:3000])

    input("ENTER PARA FECHAR")

    browser.close()
