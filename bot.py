import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Ваш токен (замените на свой)
TOKEN = '7690422797:AAFFbf6QYQRijNhbQ01eDTEj6AxbundDLAY'

# Список пользователей, которые нажали кнопку
participants = []

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
    user = query.from_user.full_name
    
    # Добавление пользователя в список участников, если его нет
    if user not in participants:
        participants.append(user)
    
    # Ответ на нажатие кнопки
    await query.answer()

    # Если нажали оба участника, то выбираем победителя
    if len(participants) >= 2:
        winner = random.choice(participants)
        await query.edit_message_text(text=f"Победитель: {winner}")
        participants.clear()  # Очищаем список участников для следующего раунда
    else:
        await query.edit_message_text(text=f"Вы нажали кнопку! Участвуют: {len(participants)}/2")

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
