import logging
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.utils.request import Request

TOKEN = "8829710593:AAHZTefZtswQMYpK9OLPamOEnp-f9WGCP_Y"

logging.basicConfig(level=logging.INFO)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я твой бот, и я наконец-то работаю в облаке!")

def echo(update: Update, context: CallbackContext):
    update.message.reply_text(f"Ты написал: {update.message.text}")

if __name__ == "__main__":
    request = Request(proxy_url=None)
    bot = Bot(token=TOKEN, request=request)
    dp = Dispatcher(bot, None, workers=0)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    
    logging.info("✅ Бот запущен и готов к работе!")
    dp.start()
    dp.idle()
