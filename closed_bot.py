import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("8350490142:AAFO-sVQt9094ogGknUakgt_zqUEO23PQm4")  # установить в окружении

async def reply_closed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Мы закрыты")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await reply_closed(update, context)

def main():
    if not TELEGRAM_TOKEN:
        print("Нужно задать переменную окружения TELEGRAM_TOKEN")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, reply_closed))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()