import telebot
import os
from dotenv import load_dotenv
from telebot import types

# Загружаем токен из .env
load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

# ID, куда будут отправляться заявки
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# Список вопросов и ответов
TARO_QA = {
    "Что происходит на консультации?": (
        "Это спокойная беседа. Ты рассказываешь, что волнует, а специалист с помощью карт помогает "
        "увидеть ситуацию под другим углом и понять себя лучше."
    ),
    "Это типа гадания?": (
        "Не совсем 🙂 Карты используются не для предсказаний, а как инструмент самоанализа. "
        "Они помогают увидеть внутренние ответы, а не будущее."
    ),
    "С какими вопросами приходят?": (
        "С самыми разными — отношения, работа, выгорание, поиск себя, неуверенность, выбор пути. "
        "Главное — желание разобраться, что происходит внутри."
    ),
    "А если нет конкретного вопроса?": (
        "Так бывает часто. Просто поговорим — и в процессе всё само прояснится."
    ),
    "Как проходит встреча?": (
        "Обычно онлайн — в Zoom или переписке. Спокойно, без давления. "
        "Ты задаёшь тему, специалист объясняет символику карт, и вместе ищете смысл."
    ),
    "Сколько стоит?": (
        "Обычно консультация длится около часа и стоит примерно 2 000 ₽. "
        "Можно начать с короткой вводной встречи, чтобы почувствовать формат."
    )
}

# Главное меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🔮 Вопросы о консультации")
    btn2 = types.KeyboardButton("💌 Хочу консультацию")
    btn3 = types.KeyboardButton("📞 Контакты")
    markup.add(btn1, btn2, btn3)
    return markup

# Подменю с вопросами
def questions_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for q in TARO_QA.keys():
        markup.add(types.KeyboardButton(q))
    markup.add(types.KeyboardButton("⬅️ Назад"))
    return markup

# Хранение временных заявок
user_requests = {}

# Стартовое сообщение
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name or 'друг'}! 👋\n"
        "Я расскажу, как проходят консультации по Таро — спокойно, без мистики.\n"
        "Выбери, с чего начать 👇",
        reply_markup=main_menu()
    )

# Основная логика
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()

    # Вопросы
    if "вопрос" in text:
        bot.send_message(
            message.chat.id,
            "Вот вопросы, которые чаще всего задают:",
            reply_markup=questions_menu()
        )

    # Контакты
    elif "контакт" in text:
        bot.send_message(
            message.chat.id,
            "📞 Связаться со специалистом можно здесь:\n"
            "Telegram: @your_taro_username\n"
            "Email: taro.consult@example.com"
        )

    # Хочу консультацию
    elif "консультац" in text:
        bot.send_message(
            message.chat.id,
            "📝 Давай оформим короткую заявку.\nКак тебя зовут?"
        )
        user_requests[message.chat.id] = {"step": "name"}

    # Если пользователь заполняет заявку
    elif message.chat.id in user_requests:
        step = user_requests[message.chat.id]["step"]

        # Шаг 1 — имя
        if step == "name":
            user_requests[message.chat.id]["name"] = message.text
            user_requests[message.chat.id]["step"] = "topic"
            bot.send_message(message.chat.id, "О чём ты хочешь поговорить на консультации?")

        # Шаг 2 — тема
        elif step == "topic":
            user_requests[message.chat.id]["topic"] = message.text
            user_requests[message.chat.id]["step"] = "contact"
            bot.send_message(message.chat.id, "Как с тобой связаться? (например, @username или телефон)")

        # Шаг 3 — контакт
        elif step == "contact":
            user_requests[message.chat.id]["contact"] = message.text

            data = user_requests[message.chat.id]
            text_request = (
                f"📩 <b>Новая заявка на консультацию</b>\n\n"
                f"👤 Имя: {data['name']}\n"
                f"💬 Тема: {data['topic']}\n"
                f"📱 Контакт: {data['contact']}\n"
                f"🔗 Пользователь: @{message.from_user.username or 'без никнейма'}"
            )

            # Отправляем админу
            if ADMIN_ID:
                bot.send_message(ADMIN_ID, text_request, parse_mode="HTML")

            bot.send_message(
                message.chat.id,
                "Спасибо! 🙌 Заявка отправлена. Специалист свяжется с тобой в ближайшее время.",
                reply_markup=main_menu()
            )
            del user_requests[message.chat.id]

    # Ответы на вопросы
    elif message.text in TARO_QA.keys():
        answer = TARO_QA[message.text]
        bot.send_message(message.chat.id, f"💬 {answer}")

    # Назад
    elif "назад" in text:
        bot.send_message(message.chat.id, "Главное меню 👇", reply_markup=main_menu())

    # Если что-то другое
    else:
        bot.send_message(
            message.chat.id,
            "Я могу рассказать о консультациях или помочь записаться 🙂\n"
            "Выбери нужный пункт из меню 👇",
            reply_markup=main_menu()
        )

# Запуск
bot.polling(none_stop=True, interval=0)
