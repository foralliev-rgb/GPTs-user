import telebot
import os
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

# 🔹 Укажи ID консультанта (можно узнать, написав @userinfobot в Telegram)
CONSULTANT_ID = int(os.getenv('CONSULTANT_ID', 0))  # пример: 123456789

# --- Вопросы и ответы ---
qa_pairs = {
    "А что вообще происходит на консультации?":
        "Обычно это спокойная беседа. Ты рассказываешь, что волнует, "
        "а специалист помогает разобраться в ситуации с помощью символов карт. "
        "Это не про предсказания, а про понимание себя и своих реакций.",

    "Это типа гадания?":
        "Не совсем 🙂 Карты используются не как инструмент предсказания, "
        "а как способ осознать, что происходит. Они помогают увидеть ситуацию под новым углом.",

    "С какими вопросами можно приходить?":
        "С любыми, где чувствуешь, что застрял — отношения, работа, выгорание, самооценка, выбор пути.",

    "А если я просто запутался, без конкретного вопроса?":
        "Так часто бывает. Во время разговора запрос сам проясняется. "
        "Иногда человек приходит просто поговорить, и уже в процессе становится понятно, что важно сейчас.",

    "Как проходит встреча?":
        "Чаще всего онлайн — в Zoom или переписке. "
        "Специалист помогает сформулировать тему, выкладывает карты, объясняет символику и ищет вместе с тобой выводы.",

    "Нужно ли верить в карты, чтобы это работало?":
        "Нет 🙂 Главное — быть готовым слушать себя. "
        "Карты — это просто способ взглянуть на ситуацию под другим углом, как зеркало.",

    "А вдруг там что-то страшное выпадет?":
        "Это миф из фильмов 🙂 Карты не предсказывают беды — "
        "они лишь отражают состояние или тенденцию. Всё зависит от интерпретации.",

    "А это безопасно психологически?":
        "Да. Консультация проходит мягко, без давления. "
        "Это не замена психотерапии, но может стать хорошим дополнением, помогая лучше понять себя.",

    "Сколько стоит такая встреча?":
        "Обычно консультация длится около часа и стоит примерно 2 000 ₽. "
        "Можно начать с короткой вводной беседы, чтобы понять формат.",

    "Как записаться, если я решу попробовать?":
        "Просто напиши: «Хочу консультацию» — и специалист свяжется с тобой, "
        "чтобы подобрать удобное время. Можно задать уточняющие вопросы прямо здесь."
}

# --- Команда /start ---
@bot.message_handler(commands=["start"])
def start(message):
    name = message.from_user.first_name or "друг"
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    for question in qa_pairs.keys():
        markup.add(telebot.types.KeyboardButton(question))

    markup.add(telebot.types.KeyboardButton("💬 Связаться со специалистом"))

    # сохраняем пользователя
    save_user(message.from_user)

    bot.send_message(
        message.chat.id,
        f"Привет, {name}! 👋\n\n"
        "Я расскажу, как проходят консультации по Таро — просто и без мистики.\n\n"
        "Выбери интересующий вопрос или нажми «💬 Связаться со специалистом».",
        reply_markup=markup
    )

# --- Сохранение данных о пользователе ---
def save_user(user):
    user_info = f"{user.id} | {user.first_name or ''} | {user.username or ''}\n"
    users_file = "users.txt"

    if not os.path.exists(users_file):
        with open(users_file, "w", encoding="utf-8") as f:
            f.write("ID | Имя | Username\n")

    with open(users_file, "a", encoding="utf-8") as f:
        f.write(user_info)

# --- Обработка сообщений ---
@bot.message_handler(content_types=["text"])
def handle_text(message):
    user_text = message.text.strip()

    if user_text in qa_pairs:
        bot.send_message(message.chat.id, qa_pairs[user_text])

    elif user_text == "💬 Связаться со специалистом":
        name = message.from_user.first_name or "Без имени"
        username = f"@{message.from_user.username}" if message.from_user.username else "(без username)"
        text = (
            f"Пользователь {name} {username} хочет связаться со специалистом.\n"
            f"ID: {message.from_user.id}"
        )
        bot.send_message(message.chat.id, "Отлично 🙌 Я передам специалисту, что ты хочешь связаться. Он напишет тебе лично.")
        if CONSULTANT_ID:
            bot.send_message(CONSULTANT_ID, f"📩 Новый запрос:\n{text}")
        else:
            print("⚠️ CONSULTANT_ID не задан. Уведомление не отправлено.")

    elif "консультац" in user_text.lower() or "запис" in user_text.lower():
        bot.send_message(
            message.chat.id,
            "Отлично 🙌 Я передам специалисту, что ты хочешь записаться. "
            "Он свяжется с тобой в ближайшее время."
        )
        if CONSULTANT_ID:
            bot.send_message(
                CONSULTANT_ID,
                f"📬 Пользователь @{message.from_user.username or 'без_username'} "
                f"({message.from_user.first_name}) написал: {user_text}"
            )

    else:
        bot.send_message(
            message.chat.id,
            "Я пока умею только рассказывать о консультациях по Таро 😊\n"
            "Попробуй выбрать один из вопросов в меню."
        )

# --- Запуск ---
if __name__ == "__main__":
    print("🤖 Бот запущен и готов к работе!")
    bot.polling(none_stop=True, interval=0)
