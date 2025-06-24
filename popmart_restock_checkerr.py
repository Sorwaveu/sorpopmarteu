# popmart_restock_checker.py

"""Pop Mart Restock Checker (Playwright Version)

Uruchamiany co 5 minut na Render.com (cron).
- Jeśli uruchomisz z flagą --test, bot wyśle TESTOWĄ wiadomość na Discord i zakończy się.
- Bez flagi sprawdza stronę produktu; gdy wykryje restock (frazy z listy KEYWORDS), wysyła powiadomienie i kończy się.
"""

import asyncio
import argparse
import requests
from playwright.async_api import async_playwright

# === KONFIGURACJA ===
PRODUCT_URL = "https://www.popmart.com/pl/products/527/THE-MONSTERS---Exciting-Macaron-Vinyl-Face-Blind-Box"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1387113098023800852/PU-X9wuGkBlb5oMBkIKP9_s2LNI10ZSTn0JnBwCKu7yJgiZ-YF8a1BQxnY4yt2QZBVAs"
KEYWORDS = [
    "in stock",
    "available",
    "restock",
    "add to cart",
    "再入荷",
    "dodaj do koszyka",
]

async def check_restock() -> bool:
    """Zwraca True, jeśli na stronie widać dowolne słowo kluczowe z KEYWORDS."""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(PRODUCT_URL, timeout=30000)
            content = await page.content()
            await browser.close()
            return any(keyword in content.lower() for keyword in KEYWORDS)
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

async def main():
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

    if await check_restock():
        send_discord_notification(f"🔔 **RESTOCK!** {PRODUCT_URL}")
    else:
        print("[INFO] Brak restocku – zakończono.")

if __name__ == "__main__":
    asyncio.run(main())
