import logging
import httpx
import asyncio
from flask import Flask
import threading

TOKEN = "8829710593:AAHZTefZtswQMYpK9OLPamOEnp-f9WGCP_Y"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

logging.basicConfig(level=logging.INFO)

# --- Веб-сервер для Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# --- Функция отправки сообщений (ИСПРАВЛЕННАЯ) ---
async def send_message(chat_id, text):
    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE_URL}/sendMessage", data={"chat_id": chat_id, "text": text})

# --- Твой Telegram бот ---
async def main():
    offset = 0
    logging.info("✅ Бот запущен! Он работает и готов отвечать!")
    
    while True:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{BASE_URL}/getUpdates", params={"offset": offset, "timeout": 30})
                data = resp.json()
                updates = data.get("result", [])
            
            for upd in updates:
                offset = upd["update_id"] + 1
                msg = upd.get("message")
                if msg and msg.get("text"):
                    chat_id = msg["chat"]["id"]
                    text = msg["text"]
                    if text == "/start":
                        await send_message(chat_id, "Привет! Бот наконец-то работает корректно!")
                    else:
                        await send_message(chat_id, f"Ты написал: {text}")
        except Exception as e:
            logging.warning(f"Ошибка: {e}")
        await asyncio.sleep(1)

if __name__ == "__main__":
    # Запускаем Flask в отдельном потоке
    threading.Thread(target=run_flask).start()
    # Запускаем основного бота
    asyncio.run(main())
