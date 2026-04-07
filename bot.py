import requests
from bs4 import BeautifulSoup
import re
import os

URL = "https://msgold.com.my/index"
TARGET = 610  # your threshold

BOT_TOKEN = os.getenv("8515843924:AAEZMv4I7Sevrv5-yylHQPjoHHRIv_7Ed0U")
CHAT_ID = os.getenv("899066821")

def get_gold_price_gram():
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # Find the exact string "999.9 Gold MYR / Gram"
    element = soup.find(string=re.compile(r"999\.9\s+Gold\s+MYR\s*/\s*Gram"))
    if not element:
        return None

    # Get the parent container (row/div) that contains the price
    parent = element.find_parent()
    if not parent:
        return None

    # Extract "WE SELL" followed by number
    text = parent.get_text(" ", strip=True).upper()  # join all child text
    match = re.search(r'WE SELL[:\s]*([\d,.]+)', text)
    if match:
        price_str = match.group(1).replace(",", "")
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
