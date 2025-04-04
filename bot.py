import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram.ext import CallbackContext

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Список для хранения пользователей, которые нажали кнопку
users = []

# Функция для обработки нажатия кнопки
async def button_press(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user not in users:
        users.append(user)
        await update.message.reply_text(f"{user.first_name} нажал первым!")

# Функция для старта бота
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Привет! Нажми кнопку, чтобы узнать, кто первый!"
    )

    # Создаем кнопку
    keyboard = [
        [InlineKeyboardButton("Нажми меня!", callback_data="press")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Нажми кнопку!", reply_markup=reply_markup
    )

def main() -> None:
    """Запуск бота."""
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    # Обработчик команд
    application.add_handler(CommandHandler("start", start))

    # Обработчик кнопок
    application.add_handler(CallbackQueryHandler(button_press, pattern="press"))

    application.run_polling()

if __name__ == "__main__":
    main()
