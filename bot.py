from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio
import os

TOKEN = os.getenv("TOKEN")  # Получаем токен из переменных окружения
first_click = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global first_click
    first_click = None  # Сбрасываем победителя перед новым раундом
    keyboard = [[InlineKeyboardButton("Жми!", callback_data="click")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Кто нажмет первым?", reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global first_click
    query = update.callback_query
    await query.answer()
    
    if first_click is None:
        first_click = query.from_user.first_name
        await context.bot.send_message(chat_id=query.message.chat_id, text=f"{first_click} нажал(а) первым!")

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    
    print("Бот запущен...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
