import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time
import os

URL = 'https://www.holland2stay.com/utrecht.html'
MAX_RENT = 900
CHECK_INTERVAL = 300  # هر 5 دقیقه

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = Bot(token=TELEGRAM_TOKEN)
sent = set()

def check_and_alert():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    listings = soup.select('.property-list .property')

    for listing in listings:
        title_el = listing.select_one('.property__title')
        price_el = listing.select_one('.property__price')
        link_el = listing.find('a')
        if not (title_el and price_el and link_el):
            continue

        title = title_el.text.strip()
        price_text = price_el.text.strip().replace("€", "").replace(",", "").split()[0]
        try:
            price = int(price_text)
        except:
            continue

        link = "https://www.holland2stay.com" + link_el['href']
        if price <= MAX_RENT and link not in sent:
            msg = f"🏠 *{title}*\n💶 {price} €\n🔗 {link}"
            bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')
            sent.add(link)

if __name__ == "__main__":
    while True:
        try:
            check_and_alert()
        except Exception as e:
            print("Error:", e)
        time.sleep(CHECK_INTERVAL)
