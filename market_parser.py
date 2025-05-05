# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

with open("markets.json", "r") as markets_file:
    market_selectors = json.load(markets_file)

# открываем маркет, эмулируем поиск
def parse_market(product_link):
    # опции браузера для обхода антибота
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # открываем окно браузера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
            """
    })

    # получаем домен из ссылки
    domain_part = product_link.split("://")[1].split("/")[0].split("?")[0]

    try:
        print("Открываю", product_link)
        driver.get(product_link)

        # обрабатываем куки аутентификации
        if market_selectors[domain_part]["cookie_file"] != 'null':
            with open(market_selectors[domain_part]["cookie_file"], "r") as cookies:
                enter_cookie = json.load(cookies)

            for c in enter_cookie:
                c.pop("sameSite", None)
                driver.add_cookie(c)

            driver.get(product_link)

        wait = WebDriverWait(driver, 10)
        time.sleep(2)

        # отладочный скрин
        driver.save_screenshot(market_selectors[domain_part]["name"] + ".png")

        market_selector = market_selectors[domain_part]
        price_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, market_selector["price"])))
        return price_input.text

    except Exception as e:
        print("Ошибка во время парсинга ", product_link, e)
        return 'null'

    finally:
        driver.quit()