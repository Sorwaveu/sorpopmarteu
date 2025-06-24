import os
import requests
from bs4 import BeautifulSoup

PRODUCT_URL = "https://www.popmart.com/pl/products/527/THE-MONSTERS---Exciting-Macaron-Vinyl-Face-Blind-Box"

# Słowa kluczowe oznaczające restock lub dostępność
KEYWORDS = [
    "in stock",
    "available",
    "restock",
    "add to cart",
    "再入荷",
    "dodaj do koszyka",
]

def check_restock():
    try:
        response = requests.get(PRODUCT_URL, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=" ").lower()

        for keyword in KEYWORDS:
            if keyword in text:
                return True
        return False
    except Exception as e:
        print(f"[BŁĄD] Nie udało się pobrać strony: {e}")
        return False

def send_discord_notification(message):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("[BŁĄD] Brak webhooka Discord w zmiennych środowiskowych!")
        return
    try:
        resp = requests.post(webhook_url, json={"content": message}, timeout=10)
        resp.raise_for_status()
        print("[INFO] Powiadomienie wysłane na Discord.")
    except Exception as e:
        print(f"[BŁĄD] Nie udało się wysłać webhooka: {e}")

def main():
    if check_restock():
        send_discord_notification(f"🔔 RESTOCK wykryty! {PRODUCT_URL}")
    else:
        print("[INFO] Brak restocku - nic do wysłania.")

if __name__ == "__main__":
    main()
