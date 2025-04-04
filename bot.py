from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import time

# Ваш токен
TOKEN = '7690422797:AAFFbf6QYQRijNhbQ01eDTEj6AxbundDLAY'

# Словарь для хранения времени нажатия кнопки и пользователей
press_times = {}

# Функция стартового сообщения
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Нажми меня!", callback_data='button_pressed')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Нажми кнопку, чтобы принять участие!', reply_markup=reply_markup)

# Функция обработки нажатия кнопки
def button(update: Update, context: CallbackContext):
    user = update.callback_query.from_user
    press_time = time.time()  # Время нажатия кнопки
    press_times[user.id] = press_time  # Сохраняем время нажатия кнопки для пользователя
    update.callback_query.answer(f"{user.first_name} нажал на кнопку!")

# Функция выбора победителя
def winner(update: Update, context: CallbackContext):
    if press_times:
        # Ищем пользователя с минимальным временем нажатия
        winner_id = min(press_times, key=press_times.get)
        winner = context.bot.get_chat_member(update.message.chat.id, winner_id).user
        update.message.reply_text(f"Победитель: {winner.first_name}!")
        # Сбрасываем данные после завершения раунда
        press_times.clear()
    else:
        update.message.reply_text("Пока никто не нажал кнопку. Начните новый раунд!")

# Функция перезапуска раунда
def restart(update: Update, context: CallbackContext):
    press_times.clear()
    start(update, context)

# Основная функция для запуска бота
def main():
    updater = Updater(TOKEN)

    # Получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрируем обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("winner", winner))
    dispatcher.add_handler(CommandHandler("restart", restart))
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Запускаем бота
    updater.start_polling()

    # Останавливаем бота на сигналы прерывания
    updater.idle()

if __name__ == '__main__':
    main()
