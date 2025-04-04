from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import time

# Список, чтобы отслеживать, кто нажал первым
press_time = None
first_press_user = None

async def start(update: Update, context):
    # Создаем кнопку
    keyboard = [
        [InlineKeyboardButton("Нажми меня", callback_data="press_button")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с кнопкой
    await update.message.reply_text("Нажми на кнопку, чтобы поиграть!", reply_markup=reply_markup)

async def button_press(update: Update, context):
    global press_time, first_press_user

    # Проверяем, был ли уже нажат кто-то
    if press_time is None:
        press_time = time.time()
        first_press_user = update.callback_query.from_user.username
        await update.callback_query.answer("Ты нажал первым!")
    else:
        # Проверяем, если кто-то уже был первым, отправляем сообщение
        if first_press_user == update.callback_query.from_user.username:
            await update.callback_query.answer("Ты уже был первым!")
        else:
            await update.callback_query.answer(f"Ты нажал кнопку, но первым был {first_press_user}.")

async def main():
    # Создаем экземпляр бота с вашим токеном
    application = Application.builder().token("7690422797:AAFFbf6QYQRijNhbQ01eDTEj6AxbundDLAY").build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_press, pattern="press
