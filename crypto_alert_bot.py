import requests
import time
from datetime import datetime
8
BOT_TOKEN = "YOUR_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

coins = ["bitcoin", "ethereum"]

targets = {
    "bitcoin": 82000,
    "ethereum": 2500
}

alert_sent = {}

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": text
        }, timeout=10)

    except Exception as e:
        print("Telegram Error:", e)

def get_prices(retries=3):

    url = "https://api.coingecko.com/api/v3/simple/price"

    for attempt in range(retries):

        try:
            response = requests.get(
                url,
                params={
                    "ids": ",".join(coins),
                    "vs_currencies": "usd"
                },
                timeout=20
            )

            return response.json()

        except requests.exceptions.Timeout:
            print(f"Timeout... Retry {attempt + 1}/{retries}")

        except Exception as e:
            print("API Error:", e)

        time.sleep(3)

    return {}

while True:
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking prices...")

    data = get_prices()

    for coin in coins:
        if coin in data and "usd" in data[coin]:

            price = data[coin]["usd"]

            print(f"{coin.capitalize()}: ${price}")

            # Prevents spam alerts
            if price >= targets[coin]:

                if not alert_sent.get(coin, False):

                    send_message(
                        f"🚨 {coin.upper()} crossed target!\nCurrent Price: ${price}"
                    )

                    print(f"Alert sent for {coin}")

                    alert_sent[coin] = True

            else:
                alert_sent[coin] = False

    time.sleep(30)