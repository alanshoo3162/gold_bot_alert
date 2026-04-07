import requests
from bs4 import BeautifulSoup
import os

URL = "https://msgold.com.my/index"
TARGET = 610  # your threshold

BOT_TOKEN = os.getenv("8515843924:AAEZMv4I7Sevrv5-yylHQPjoHHRIv_7Ed0U")
CHAT_ID = os.getenv("99066821")

def get_gold_price_999():
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # Find the table row that contains "999"
    rows = soup.find_all("tr")
    for row in rows:
        if "999" in row.get_text():
            # Find the "WE SELL" price, usually the 2nd or 3rd <td>
            cells = row.find_all("td")
            for i, cell in enumerate(cells):
                if "WE SELL" in cell.get_text().upper():
                    # price is in the next <td>
                    price_cell = cells[i + 1].get_text().strip()
                    price_cell = price_cell.replace(",", "")  # remove thousand separators
                    try:
                        return float(price_cell)
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
    price = get_gold_price_999()
    print("Gold 999 WE SELL:", price)
    if price and price >= TARGET:
        send_telegram(f"🚨 MS Gold 999 Alert! RM {price}")

if __name__ == "__main__":
    main()
