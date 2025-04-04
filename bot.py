from telegram.ext import Application, CommandHandler
import logging

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Определяем команды
async def start(update, context):
    await update.message.reply_text('Привет! Я бот.')

# Основная функция
if __name__ == "__main__":
    # Токен бота
    token = 'YOUR_BOT_TOKEN'

    # Создаем экземпляр бота
    app = Application.builder().token(token).build()

    # Добавляем обработчик команд
    app.add_handler(CommandHandler("start", start))

    # Запускаем polling для получения сообщений
    app.run_polling()
