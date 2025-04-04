import random
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Ваш токен (замените на свой)
TOKEN = '7690422797:AAFFbf6QYQRijNhbQ01eDTEj6AxbundDLAY'

# Список участников с временем нажатия
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
    await update.message.reply_text('Нажмите кнопку, чтобы принять участие в розыгрыше!', reply_markup=reply_markup)

# Функция для обработки нажатия кнопки
async def button(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    timestamp = time.time()  # Текущее время в секундах

    # Если пользователь еще не нажимал кнопку, добавляем его в список с меткой времени
    if user_id not in [participant['user_id'] for participant in participants]:
        participants.append({'user_id': user_id, 'timestamp': timestamp})
    
    # Подтверждаем, что кнопка нажата
    await update.callback_query.answer(f'Вы участвуете в розыгрыше!')

# Функция для выбора победителя (по времени нажатия кнопки)
async def pick_winner(update: Update, context: CallbackContext) -> None:
    if len(participants) < 2:
        await update.message.reply_text('Недостаточно участников для розыгрыша.')
        return
    
    # Сортируем участников по времени нажатия кнопки (первый, кто нажал, будет первым в списке)
    participants_sorted = sorted(participants, key=lambda x: x['timestamp'])
    
    # Победитель - это первый в отсортированном списке
    winner_id = participants_sorted[0]['user_id']
    winner = await context.bot.get_chat_member(update.message.chat.id, winner_id)
    
    # Отправляем сообщение о победителе
    await update.message.reply_text(f'Победитель: {winner.user.full_name} ({winner.user.username if winner.user.username else "без имени"})')
    
    # Очищаем список участников для следующего раунда
    participants.clear()

# Функция для перезапуска бота
async def reset(update: Update, context: CallbackContext) -> None:
    participants.clear()
    
    # Отправляем сообщение, чтобы все участники могли снова нажать кнопку
    keyboard = [
        [InlineKeyboardButton("Нажми меня!", callback_data='button_pressed')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text('Раунд завершен! Начинаем новый розыгрыш. Нажмите кнопку, чтобы участвовать снова.', reply_markup=reply_markup)

# Основная функция, где настраиваем обработчики команд
def main() -> None:
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button, pattern='button_pressed'))
    application.add_handler(CommandHandler("reset", reset))  # Команда для перезапуска
    application.add_handler(CommandHandler("winner", pick_winner))  # Команда для выбора победителя

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
