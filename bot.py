from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask, request
import asyncio
from threading import Lock
import logging
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Твой токен
TOKEN = '7690422797:AAFFbf6QYQRijNhbQ01eDTEj6AxbundDLAY'

# Глобальная переменная для хранения первого пользователя и блокировка
first_user = None
lock = Lock()

# Создаём Flask приложение
app = Flask(__name__)

# Создаём объект Application для бота
application = Application.builder().token(TOKEN).build()

# Функция для старта
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Нажми на меня", callback_data='button_press')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Нажми кнопку, чтобы участвовать:', reply_markup=reply_markup)

# Функция обработки нажатия на кнопку
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global first_user
    query = update.callback_query
    await query.answer()  # Подтверждение нажатия

    with lock:
        if first_user is None:
            first_user = query.from_user.first_name
            await query.edit_message_text(
                text=f'Победитель: {first_user}! Новый раунд начинается...'
            )
            logger.info(f"Winner: {first_user}")
            await asyncio.sleep(1)  # Задержка для читаемости
            keyboard = [
                [InlineKeyboardButton("Нажми на меня", callback_data='button_press')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text('Нажми снова:', reply_markup=reply_markup)
            first_user = None  # Сбрасываем для нового раунда
            logger.info("New round started, first_user reset")
        else:
            await query.edit_message_text(
                text=f'Победитель уже есть: {first_user}. Жди новый раунд!'
            )

# Health Check эндпоинт для render.com
@app.route('/healthz', methods=['GET'])
def healthz():
    logger.info("Health check requested")
    return 'OK', 200

# Обработка вебхуков через Flask
@app.route('/webhook', methods=['POST'])
async def webhook():
    logger.info("Webhook received")
    update = Update.de_json(request.get_json(), application.bot)
    await application.process_update(update)
    return 'OK', 200

# Основная функция
async def main():
    # Регистрация хендлеров
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Установка вебхука
    webhook_url = 'https://mytgbot-tzu6.onrender.com/webhook'
    try:
        await application.bot.set_webhook(url=webhook_url)
        logger.info(f"Webhook set successfully to {webhook_url}")
    except Exception as e:
        logger.error(f"Failed to set webhook: {e}")

    # Запуск Flask приложения с динамическим портом
    port = int(os.environ.get("PORT", 8443))  # Render предоставляет PORT, иначе 8443
    logger.info(f"Starting Flask server on port {port}...")
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    asyncio.run(main())