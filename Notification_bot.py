from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = '7799373154:AAGtLDeSLLAE11IM_P7guFUOb_GiyxGMEds'

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот. Здесь можно получить уведомления.")

# Основная функция
def main():
    # Создаем объект приложения
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()
