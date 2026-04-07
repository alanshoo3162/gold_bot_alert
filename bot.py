import requests
from bs4 import BeautifulSoup
import os

URL = "https://msgold.com.my/index"
TARGET = 610  # your threshold

BOT_TOKEN = os.getenv("8515843924:AAEZMv4I7Sevrv5-yylHQPjoHHRIv_7Ed0U")
CHAT_ID = os.getenv("899066821")

def get_gold_price_gram():
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # Find all table rows
    rows = soup.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        # Look for the exact item
        for i, cell in enumerate(cells):
            if "999.9 Gold MYR / Gram" in cell.get_text():
                # WE SELL is usually the next cell
                if i + 1 < len(cells):
                    price_str = cells[i + 1].get_text().strip().replace(",", "")
                    try:
                        return float(price_str)
                    except:
                        return None
    return None

def send_telegram(msg):
    import requests
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": msg}
    )

def main():
    price = get_gold_price_gram()
    print("Gold 999.9 MYR / Gram WE SELL:", price)
    if price and price >= TARGET:
        send_telegram(f"🚨 MS Gold 999.9 MYR / Gram Alert! RM {price}")

if __name__ == "__main__":
    main()
