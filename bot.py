from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Ваш токен
TOKEN = '7690422797:AAFFbf6QYQRijNhbQ01eDTEj6AxbundDLAY'

# Создание приложения (это заменяет создание Dispatcher)
app = Application.builder().token(TOKEN).build()

# Пример обработчика команды /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Привет!')

# Пример обработчика кнопки (CallbackQuery)
async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Вы нажали: {query.data}")

# Регистрируем обработчики
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

# Запуск бота
app.run_polling()
