import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Включаем логирование
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота
TOKEN = "7690422797:AAFFbf6QYQRijNhbQ01eDTEj6AxbundDLAY"

# Команда /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Я твой бот.")

# Основная функция для запуска бота
async def main():
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Запускаем бота
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
