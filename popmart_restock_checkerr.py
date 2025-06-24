# popmart_restock_checker.py

"""Pop Mart Restock Checker

Uruchamiany co 5 minut na Render.com (cron).  
- Jeśli uruchomisz z flagą --test, bot wyśle TESTOWĄ wiadomość na Discord i zakończy się.  
- Bez flagi sprawdza stronę produktu; gdy wykryje restock (frazy z listy KEYWORDS), wysyła powiadomienie i kończy się.
"""

import time
import argparse
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# === KONFIGURACJA ===
PRODUCT_URL = "https://www.popmart.com/pl/products/527/THE-MONSTERS---Exciting-Macaron-Vinyl-Face-Blind-Box"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your_webhook_here"
KEYWORDS = [
    "in stock",
    "available",
    "restock",
    "add to cart",
    "再入荷",
    "dodaj do koszyka",
]

# === SELENIUM (headless Chrome) ===
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Render.com nie udostępnia GUI, ale headless Chrome działa poprawnie.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def check_restock() -> bool:
    """Zwraca True, jeśli na stronie widać dowolne słowo kluczowe z KEYWORDS."""
    try:
        driver.get(PRODUCT_URL)
        time.sleep(5)  # czekamy, aż JS dociągnie treść
        page_text = driver.page_source.lower()
        return any(keyword in page_text for keyword in KEYWORDS)
    except Exception as exc:
        print(f"[BŁĄD] Nie udało się pobrać strony: {exc}")
        return False

def send_discord_notification(message: str) -> None:
    """Wysyła wiadomość na kanał Discord przez webhook."""
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json={"content": message}, timeout=10)
        response.raise_for_status()
        print("[INFO] Wysłano powiadomienie na Discord.")
    except Exception as exc:
        print(f"[BŁĄD] Nie udało się wysłać webhooka: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Pop Mart Restock Checker")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Wyślij testowe powiadomienie i zakończ (sprawdzenie webhooka)",
    )
    args = parser.parse_args()

    if args.test:
        send_discord_notification("✅ TEST: Webhook działa! (Pop Mart Restock Checker)")
        return

    if check_restock():
        send_discord_notification(f"🔔 **RESTOCK!** {PRODUCT_URL}")
    else:
        print("[INFO] Brak restocku – zakończono.")


if __name__ == "__main__":
    main()
