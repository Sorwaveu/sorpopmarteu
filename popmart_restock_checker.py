import requests
from bs4 import BeautifulSoup

PRODUCT_URL = "https://www.popmart.com/pl/products/527/THE-MONSTERS---Exciting-Macaron-Vinyl-Face-Blind-Box"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1387113098023800852/PU-X9wuGkBlb5oMBkIKP9_s2LNI10ZSTn0JnBwCKu7yJgiZ-YF8a1BQxnY4yt2QZBVAs"

# Frazy do wykrycia restocku lub dostępności
KEYWORDS = [
    "in stock",
    "available",
    "restock",
    "add to cart",
    "再入荷",           # japońskie 'restock'
    "dodaj do koszyka",
    "w sprzedaży",
    "dostępny",
    "już wkrótce",
    "niedostępny",
    "coming soon",
]

def check_restock():
    try:
        response = requests.get(PRODUCT_URL, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=" ").lower()
        for keyword in KEYWORDS:
            if keyword.lower() in text:
                print(f"[INFO] Wykryto frazę: {keyword}")
                return True
        return False
    except Exception as e:
        print(f"[BŁĄD] Nie udało się pobrać strony: {e}")
        return False

def send_discord_notification(message):
    try:
        r = requests.post(DISCORD_WEBHOOK_URL, json={"content": message}, timeout=10)
        r.raise_for_status()
        print("[INFO] Wysłano powiadomienie na Discord.")
    except Exception as e:
        print(f"[BŁĄD] Nie udało się wysłać powiadomienia: {e}")

def main():
    if check_restock():
        send_discord_notification(f"🔔 RESTOCK lub informacja o dostępności na stronie:\n{PRODUCT_URL}")
    else:
        print("[INFO] Restock niedostępny - nic do wysłania.")

if __name__ == "__main__":
    main()
