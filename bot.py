import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler

app = Flask(__name__)

TOKEN = "7690422797:AAFFbf6QYQRijNhbQ01eDTEj6AxbundDLAY"  # Это твой токен
WEBHOOK_URL = "https://mytgbot-tzu6.onrender.com"  # Это твой URL на Render, который ты мне прислал

bot = Bot(TOKEN)

def start(update: Update, context):
    update.message.reply_text("Привет! Нажми кнопку, чтобы сыграть.")

def button(update: Update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Победитель: {query.from_user.full_name}")

dispatcher = Dispatcher(bot, update_queue=None)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(button))

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

if __name__ == "__main__":
    bot.set_webhook(url=WEBHOOK_URL + "/webhook")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
