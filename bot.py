import logging
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from telegram.ext import Dispatcher
from telegram.ext import CallbackContext
from telegram.ext import Update
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os

# Вставьте сюда свой токен
TOKEN = "7690422797:AAFFbf6QYQRijNhbQ01eDTEj6AxbundDLAY"
WEBHOOK_URL = "https://mytgbot-tzu6.onrender.com"  # Ваш URL на Render

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Нажми кнопку, чтобы сыграть.")

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Победитель: {query.from_user.full_name}")

def main() -> None:
    """Запуск бота с настройкой вебхуков."""
    bot = Bot(TOKEN)
    
    # Устанавливаем вебхук
    bot.set_webhook(url=WEBHOOK_URL)

    # Создаем обновления
    updater = Updater(TOKEN)
    
    # Получаем диспетчер
    dispatcher = updater.dispatcher

    # Команда start
    dispatcher.add_handler(CommandHandler("start", start))

    # Кнопка
    button_handler = CallbackQueryHandler(button)
    dispatcher.add_handler(button_handler)

    # Начинаем слушать обновления
    updater.start_polling()

if __name__ == '__main__':
    main()
