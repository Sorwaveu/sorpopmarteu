# popmart_restock_checker.py

import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# === KONFIGURACJA ===
PRODUCT_URL = "https://www.popmart.com/pl/products/527/THE-MONSTERS---Exciting-Macaron-Vinyl-Face-Blind-Box"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1387113098023800852/PU-X9wuGkBlb5oMBkIKP9_s2LNI10ZSTn0JnBwCKu7yJgiZ-YF8a1BQxnY4yt2QZBVAs"
KEYWORDS = ["in stock", "available", "restock", "add to cart", "再入荷", "dodaj do koszyka"]

# === KONFIGURACJA SELENIUM ===
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Ustawienia render-friendly (no GUI)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def check_restock():
    try:
        driver.get(PRODUCT_URL)
        time.sleep(5)  # Poczekaj na JS
        page_text = driver.page_source.lower()
        return any(keyword in page_text for keyword in KEYWORDS)
    except Exception as e:
        print("[BŁĄD] Nie udalo sie załadować strony:", e)
        return False

def send_discord_notification():
    try:
        payload = {"content": f"\ud83d\udd14 **RESTOCK na Pop Mart!** {PRODUCT_URL}"}
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print("[INFO] Wyslano powiadomienie na Discord.")
    except Exception as e:
        print("[BŁĄD] Nie udalo sie wyslac webhooka:", e)

if __name__ == "__main__":
    if check_restock():
        send_discord_notification()
    else:
        print("[INFO] Brak restocku.")
