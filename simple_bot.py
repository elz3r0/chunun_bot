import logging
import sqlite3
from datetime import datetime
from flask import Flask
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8829710593:AAHZTefZtswQMYpK9OLPamOEnp-f9WGCP_Y"

logging.basicConfig(level=logging.INFO)

# --- Веб-сервер для Render ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# --- База данных ---
def init_db():
    conn = sqlite3.connect('mood.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS moods (
            user_id INTEGER,
            date TEXT,
            mood INTEGER,
            comment TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_mood(user_id, mood, comment=""):
    conn = sqlite3.connect('mood.db')
    c = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d")
    c.execute("INSERT INTO moods (user_id, date, mood, comment) VALUES (?, ?, ?, ?)",
              (user_id, date, mood, comment))
    conn.commit()
    conn.close()

def get_stats(user_id):
    conn = sqlite3.connect('mood.db')
    c = conn.cursor()
    c.execute("SELECT date, mood, comment FROM moods WHERE user_id = ? ORDER BY date DESC LIMIT 7", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

# --- Команды бота ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой трекер настроения.\n"
        "/mood [число] [комментарий] — записать день\n"
        "/stats — показать статистику"
    )

async def mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if not args:
            await update.message.reply_text("Пример: /mood 8 отличный день")
            return
        score = int(args[0])
        if score < 1 or score > 10:
            await update.message.reply_text("Оценка должна быть от 1 до 10.")
            return
        comment = " ".join(args[1:]) if len(args) > 1 else ""
        save_mood(update.effective_user.id, score, comment)
        await update.message.reply_text(f"✅ Записал! Настроение: {score}/10")
    except ValueError:
        await update.message.reply_text("Ошибка! Напиши /mood 8")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = get_stats(update.effective_user.id)
    if not rows:
        await update.message.reply_text("Пока нет записей. Напиши /mood")
        return
    msg = "📊 Последние 7 дней:\n"
    for row in rows:
        msg += f"{row[0]} — {row[1]}/10"
        if row[2]:
            msg += f" ({row[2]})"
        msg += "\n"
    await update.message.reply_text(msg)

# --- Запуск ---
if __name__ == "__main__":
    init_db()
    threading.Thread(target=run_flask).start()
    
    app_bot = Application.builder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("mood", mood))
    app_bot.add_handler(CommandHandler("stats", stats))
    
    logging.info("✅ Бот с трекером настроения запущен!")
    app_bot.run_polling()
