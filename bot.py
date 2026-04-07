import requests
from bs4 import BeautifulSoup
import re
import os

URL = "https://msgold.com.my/index"

TARGET = 630  # CHANGE THIS

BOT_TOKEN = os.getenv("8515843924:AAEZMv4I7Sevrv5-yylHQPjoHHRIv_7Ed0U")
CHAT_ID = os.getenv("899066821")

def get_gold_price():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    text = soup.get_text(separator=" ")

    # Extract all RM prices
    matches = re.findall(r'(\d{3,4}\.\d{1,2})', text)

    prices = [float(m) for m in matches]

    # Filter realistic gold price range
    prices = [p for p in prices if 300 < p < 1000]

    if prices:
        return max(prices)

    return None

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.get(url, params={
        "chat_id": CHAT_ID,
        "text": msg
    })

def main():
    price = get_gold_price()
    print("Gold:", price)

    if price and price >= TARGET:
        send_telegram(f"🚨 MS Gold Alert! RM {price}")

if __name__ == "__main__":
    main()
