import logging
import httpx
import asyncio

TOKEN = "8829710593:AAHZTefZtswQMYpK9OLPamOEnp-f9WGCP_Y"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

logging.basicConfig(level=logging.INFO)

async def send_message(chat_id, text):
    await httpx.post(f"{BASE_URL}/sendMessage", data={"chat_id": chat_id, "text": text})

async def main():
    offset = 0
    logging.info("✅ Бот запущен! Он работает и готов отвечать!")
    
    while True:
        try:
            resp = await httpx.get(f"{BASE_URL}/getUpdates", params={"offset": offset, "timeout": 30})
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
    asyncio.run(main())
