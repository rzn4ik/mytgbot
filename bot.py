from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
import time

# Ваш токен
TOKEN = '7690422797:AAFFbf6QYQRijNhbQ01eDTEj6AxbundDLAY'

# Словарь для хранения времени нажатия кнопки и пользователей
press_times = {}

# Функция стартового сообщения
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Нажми меня!", callback_data='button_pressed')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Нажми кнопку, чтобы принять участие!', reply_markup=reply_markup)

# Функция обработки нажатия кнопки
async def button(update: Update, context: CallbackContext):
    user = update.callback_query.from_user
    press_time = time.time()  # Время нажатия кнопки
    press_times[user.id] = press_time  # Сохраняем время нажатия кнопки для пользователя
    await update.callback_query.answer(f"{user.first_name} нажал на кнопку!")

# Функция выбора победителя
async def winner(update: Update, context: CallbackContext):
    if press_times:
        # Ищем пользователя с минимальным временем нажатия
        winner_id = min(press_times, key=press_times.get)
        winner = await context.bot.get_chat_member(update.message.chat.id, winner_id).user
        await update.message.reply_text(f"Победитель: {winner.first_name}!")
        # Сбрасываем данные после завершения раунда
        press_times.clear()
    else:
        await update.message.reply_text("Пока никто не нажал кнопку. Начните новый раунд!")

# Функция перезапуска раунда
async def restart(update: Update, context: CallbackContext):
    press_times.clear()
    await start(update, context)

# Основная функция для запуска бота
def main():
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("winner", winner))
    application.add_handler(CommandHandler("restart", restart))
    application.add_handler(CallbackQueryHandler(button))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
