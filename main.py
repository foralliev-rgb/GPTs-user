import os
import asyncio
from typing import List

import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Настройки: перед запуском установите переменные окружения TELEGRAM_TOKEN и OPENAI_API_KEY
TELEGRAM_TOKEN = os.environ.get("8350490142:AAFO-sVQt9094ogGknUakgt_zqUEO23PQm4")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Простейший набор ключевых слов для определения, относится ли вопрос к магазину
ALLOWED_KEYWORDS: List[str] = [
    "товар", "цена", "цены", "доставка", "возврат", "гарантия", "заказ", "наличие",
    "оплата", "самовывоз", "работа", "режим", "скидк", "купить", "ассортимент",
    "магазин", "менеджер", "доставка", "служба поддержки", "pickup"
]

SYSTEM_PROMPT = (
    "Вы — менеджер магазина. Отвечайте кратко, профессионально и по существу на вопросы, "
    "связанные только с работой магазина (товары, цены, доставка, возврат, оплата, режим работы и т.п.). "
    "Если вопрос НЕ относится к теме магазина — вежливо откажите, написав: "
    "'Извините, я могу отвечать только на вопросы, связанные с магазином.'"
)

def message_is_store_related(text: str) -> bool:
    t = text.lower()
    for kw in ALLOWED_KEYWORDS:
        if kw in t:
            return True
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Я — менеджер магазина (бот). Задавайте вопросы о товарах, ценах, доставке, возвратах и т.д."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Вопросы только по теме магазина. Пример: 'Какая цена на товар X?'")

async def ask_openai(user_text: str) -> str:
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4",  # при необходимости замените модель
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            max_tokens=500,
            temperature=0.2
        )
        return resp["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "Произошла ошибка при запросе к языковой модели."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text or ""
    if not user_text.strip():
        await update.message.reply_text("Пожалуйста, задайте вопрос.")
        return

    if not message_is_store_related(user_text):
        await update.message.reply_text("Извините, я могу отвечать только на вопросы, связанные с магазином.")
        return

    await update.message.chat.send_action(action="typing")
    answer = await asyncio.get_event_loop().run_in_executor(None, lambda: asyncio.run(ask_openai(user_text)))
    await update.message.reply_text(answer)

def main():
    if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
        print("Нужно задать переменные окружения TELEGRAM_TOKEN и OPENAI_API_KEY")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()

