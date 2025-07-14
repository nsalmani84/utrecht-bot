import asyncio
from telegram import Bot
import os

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = int(os.getenv('CHAT_ID'))

bot = Bot(token=TELEGRAM_TOKEN)

async def send_test_message():
    try:
        await bot.send_message(chat_id=CHAT_ID, text="✅ تست موفق: بات تلگرام به درستی کار می‌کند!")
        print("✅ پیام با موفقیت ارسال شد.")
    except Exception as e:
        print("❌ خطا در ارسال پیام:", e)

if __name__ == "__main__":
    asyncio.run(send_test_message())
