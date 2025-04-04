from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Ваш токен
TOKEN = '7690422797:AAFFbf6QYQRijNhbQ01eDTEj6AxbundDLAY'

# Создаем приложение
app = Application.builder().token(TOKEN).build()

# Словарь для хранения информации о первом, кто нажал кнопку
first_click_user = None

# Команда /start
async def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Нажми меня!", callback_data='press')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Привет! Нажми на кнопку.", reply_markup=reply_markup)

# Обработчик нажатия кнопки
async def button(update: Update, context: CallbackContext):
    global first_click_user

    query = update.callback_query
    user = query.from_user

    # Если это первый пользователь, кто нажал кнопку
    if first_click_user is None:
        first_click_user = user.first_name  # Сохраняем имя первого пользователя
        await query.answer()
        await query.edit_message_text(f"Первый кто нажал: {first_click_user}")
    else:
        await query.answer()
        await query.edit_message_text(f"Первый кто нажал: {first_click_user}. Твой ход, {user.first_name}!")

# Регистрируем обработчики
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

# Запуск бота
app.run_polling()
