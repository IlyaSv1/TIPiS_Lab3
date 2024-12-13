from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '7799373154:AAGtLDeSLLAE11IM_P7guFUOb_GiyxGMEds'

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Вы можете отправить мне свою геопозицию, и я её обработаю.")

# Команда /location
# async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     latitude = 55.7558  # Широта
#     longitude = 37.6173  # Долгота
    
#     # Используем sendLocation
#     await context.bot.send_location(chat_id=update.effective_chat.id, latitude=latitude, longitude=longitude)
#     await update.message.reply_text("Вот координаты местоположения!")

# Обработка локации пользователя
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_location = update.message.location
    latitude = user_location.latitude
    longitude = user_location.longitude

    # Отправляем локацию пользователю
    await context.bot.send_location(
        chat_id=update.effective_chat.id, latitude=latitude, longitude=longitude
    )
    await update.message.reply_text(
        f"Я получил вашу локацию:\n"
        f"Широта: {latitude}\n"
        f"Долгота: {longitude}"
    )

# Основная функция
def main():
    # Создаем объект приложения
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))

    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()
