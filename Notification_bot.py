from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

TOKEN = "7799373154:AAGtLDeSLLAE11IM_P7guFUOb_GiyxGMEds"


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот. Я буду напоминать вам отправить вашу геопозицию."
    )

    # Кнопка для отправки геопозиции
    location_button = KeyboardButton(text="Отправить геопозицию", request_location=True)
    reply_markup = ReplyKeyboardMarkup([[location_button]], resize_keyboard=True)

    await update.message.reply_text(
        "Нажмите на кнопку ниже, чтобы отправить свою геопозицию.",
        reply_markup=reply_markup,
    )

    # Добавляем задачу на отправку напоминания каждые 30 секунд
    job = context.job_queue.run_repeating(
        send_location_request, interval=30, first=0, data=update.message.chat.id
    )
    # Сохраняем задачу в контексте для доступа к ней в команде /stop
    context.chat_data["job"] = job


# Функция отправки запроса на геопозицию
async def send_location_request(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data
    await context.bot.send_message(
        chat_id=chat_id, text="Пожалуйста, отправьте свою геопозицию!"
    )


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
        f"Я получил вашу локацию:\n" f"Широта: {latitude}\n" f"Долгота: {longitude}"
    )


# Команда /stop для остановки бота
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем, есть ли сохраненная задача
    job = context.chat_data.get("job")
    if job:
        job.schedule_removal()  # Останавливаем задачу
        del context.chat_data["job"]  # Удаляем задачу из контекста
        await update.message.reply_text("Напоминания остановлены.")
    else:
        await update.message.reply_text("Нет активных напоминаний.")

    # Завершаем работу бота
    await update.message.reply_text("Бот остановлен.")
    context.application.stop()  # Останавливаем работу бота


# Основная функция
def main():
    # Создаем объект приложения
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        CommandHandler("stop", stop)
    )  # Добавляем обработчик для /stop
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))

    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()


if __name__ == "__main__":
    main()
