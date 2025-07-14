import requests
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio
import os

URL = 'https://www.holland2stay.com/utrecht.html'
MAX_RENT = 900
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
        price_el = listing.select_one('.property__pric
