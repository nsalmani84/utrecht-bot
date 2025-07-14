import requests
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio
import os

URL = 'https://www.holland2stay.com/utrecht.html'
MAX_RENT = 2000
CHECK_INTERVAL = 300  # هر 5 دقیقه

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = int(os.getenv('CHAT_ID'))

bot = Bot(token=TELEGRAM_TOKEN)
sent = set()

async def check_and_alert():
    global sent
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
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
            await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')
            sent.add(link)
            print(f"✅ پیام ارسال شد برای: {title}")

async def main():
    while True:
        try:
            await check_and_alert()
        except Exception as e:
            print("❌ خطا:", e)
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    asyncio.run(main())
