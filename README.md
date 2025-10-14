from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 🔹 Твой токен от BotFather
TOKEN = "8350490142:AAFO-sVQt9094ogGknUakgt_zqUEO23PQm4"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой бот 😊")

# Ответ на любое сообщение
async def reply_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    if "привет" in user_text:
        await update.message.reply_text("Привет! Рад тебя видеть 👋")
    else:
        await update.message.reply_text("Я тебя понял, но лучше скажи 'привет' 😉")

# Основная функция запуска
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_message))

    print("✅ Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()

