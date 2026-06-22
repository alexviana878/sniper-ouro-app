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

    input("APERTE ENTER PARA FECHAR")

    browser.close()
