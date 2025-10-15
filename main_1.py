import telebot
import os
from dotenv import load_dotenv
from telebot import types

load_dotenv()  # Загружаем .env файл

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

# Простая "база данных" GPT-агентов
GPT_PRODUCTS = {
    "GPT Start": {
        "описание": "Базовый агент для чата и ответов на вопросы.",
        "цена": "10 у.е./мес"
    },
    "GPT Pro": {
        "описание": "Продвинутый агент с возможностью интеграции в Telegram и CRM.",
        "цена": "50 у.е./мес"
    },
    "GPT Business": {
        "описание": "Многофункциональный агент для бизнеса, аналитики и поддержки клиентов.",
        "цена": "100 у.е./мес"
    }
}

# Ключевые слова для определения релевантных сообщений
GPT_KEYWORDS = ["gpt", "агент", "бот", "assistant", "чат", "модель", "продажа", "купить", "стоимость", "менеджер"]

# Главное меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🛍️ Каталог GPT-агентов")
    btn2 = types.KeyboardButton("💰 Цены")
    btn3 = types.KeyboardButton("📞 Контакты")
    btn4 = types.KeyboardButton("❓ Консультация")
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    return markup

# Стартовое сообщение
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Здравствуйте! 👋 Я менеджер магазина GPT’s-агентов.\n"
        "Я помогу подобрать подходящего агента под ваши задачи.\n"
        "Выберите интересующий раздел ниже:",
        reply_markup=main_menu()
    )

# Обработка кнопок меню
@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    text = message.text.lower()

    # Каталог
    if "каталог" in text:
        response = "🧠 Доступные GPT-агенты:\n\n"
        for name, info in GPT_PRODUCTS.items():
            response += f"**{name}**\n{info['описание']}\n💰 {info['цена']}\n\n"
        bot.send_message(message.chat.id, response, parse_mode="Markdown")

    # Цены
    elif "цены" in text or "стоимость" in text:
        bot.send_message(
            message.chat.id,
            "💰 Наши GPT-агенты по подписке:\n"
            "• GPT Start — 10 у.е./мес\n"
            "• GPT Pro — 50 у.е./мес\n"
            "• GPT Business — 100 у.е./мес\n"
            "\nВыберите подходящий в разделе 'Каталог'."
        )

    # Контакты
    elif "контакты" in text:
        bot.send_message(
            message.chat.id,
            "📞 Связаться с менеджером:\nTelegram: @gptshop_support\nEmail: support@gptshop.ai"
        )

    # Консультация
    elif "консультация" in text:
        bot.send_message(
            message.chat.id,
            "🗣 Напишите, для каких целей вам нужен GPT-агент — и я помогу подобрать лучший вариант!"
        )

    # Проверка на релевантность темы
    elif any(keyword in text for keyword in GPT_KEYWORDS):
        bot.send_message(
            message.chat.id,
            "Я рад, что вы интересуетесь нашими GPT-агентами! 💡\n"
            "Могу рассказать про функции, стоимость или интеграцию."
        )

    # Если вопрос не по теме — бот отказывает
    else:
        bot.send_message(
            message.chat.id,
            "Извините 🙏, я консультирую только по вопросам, связанным с GPT-агентами.\n"
            "Пожалуйста, выберите пункт из меню."
        )

# Запуск бота
bot.polling(none_stop=True, interval=0)
