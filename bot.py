from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Ваш токен (замените на свой)
TOKEN = '7690422797:AAFFbf6QYQRijNhbQ01eDTEj6AxbundDLAY'

# Функция обработки команды /start
async def start(update: Update, context: CallbackContext) -> None:
    # Создание кнопки
    keyboard = [
        [InlineKeyboardButton("Нажми меня!", callback_data='button_pressed')]
    ]
    
    # Создание разметки для кнопки
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Отправка сообщения с кнопкой
    await update.message.reply_text('Привет! Нажми на кнопку ниже:', reply_markup=reply_markup)

# Функция для обработки нажатия на кнопку
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    # Ответ на нажатие кнопки
    await query.answer()
    # Ответ с текстом о том, кто нажал на кнопку
    await query.edit_message_text(text=f"Кнопку нажал: {query.from_user.full_name}")

# Основная функция
def main() -> None:
    # Инициализация приложения с токеном
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    application.run_polling()

# Запуск бота, если это основной скрипт
if __name__ == '__main__':
    main()
