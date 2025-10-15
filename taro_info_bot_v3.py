import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# 🔹 Укажи свой токен и ID (куда бот будет отправлять заявки)
API_TOKEN = "8478841875:AAGg0XIIbQ_OamBOHW3TEYRe_WODE7A4KuE"
ADMIN_ID = @IEvgeniyV  # ← замени на свой Telegram ID (можно узнать у @userinfobot)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 🔹 FSM (машина состояний для заявки)
class RequestForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_topic = State()
    waiting_for_contact = State()

# 🔹 Вопросы и ответы
qa_pairs = [
    ("А что вообще происходит на консультации?",
     "Это спокойная беседа. Ты рассказываешь, что волнует, а специалист помогает разобраться через символику карт. Всё без мистики — фокус на понимании себя."),

    ("Это типа гадания?",
     "Не совсем 🙂 Карты используются не для предсказаний, а для анализа. Они помогают взглянуть на ситуацию под новым углом и найти внутренние ответы."),

    ("С какими вопросами можно приходить?",
     "С любыми: отношения, работа, выгорание, выбор пути. Всё, где важно разобраться и почувствовать уверенность."),

    ("А если нет чёткого вопроса?",
     "Так бывает часто. Во время разговора всё само проясняется. Иногда важно просто начать диалог, и понимание приходит само."),

    ("Как проходит встреча?",
     "Обычно онлайн — в Zoom или переписке. Специалист помогает сформулировать тему, выкладывает карты и обсуждает, что они могут символизировать."),
]

# 🔹 /start
@dp.message(Command("start"))
async def start(message: types.Message):
    name = message.from_user.first_name or "друг"
    kb = InlineKeyboardBuilder()
    for i, (q, _) in enumerate(qa_pairs):
        kb.button(text=q, callback_data=f"q_{i}")
    kb.button(text="💌 Хочу консультацию", callback_data="consult")
    kb.adjust(1)
    await message.answer(
        f"Привет, {name}! 👋\nЯ помогу тебе разобраться, как проходят консультации по Таро.\n\nВыбери вопрос или запишись на консультацию:",
        reply_markup=kb.as_markup()
    )

# 🔹 Ответы
@dp.callback_query(lambda c: c.data.startswith("q_"))
async def show_answer(callback: types.CallbackQuery):
    i = int(callback.data.split("_")[1])
    q, a = qa_pairs[i]
    kb = InlineKeyboardBuilder()
    kb.button(text="💌 Записаться", callback_data="consult")
    kb.adjust(1)
    await callback.message.answer(f"❓ <b>{q}</b>\n\n💬 {a}", parse_mode="HTML", reply_markup=kb.as_markup())

# 🔹 Начало заявки
@dp.callback_query(lambda c: c.data == "consult")
async def start_request(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Давай оформим короткую заявку 📝\n\nКак тебя зовут?")
    await state.set_state(RequestForm.waiting_for_name)

# 🔹 Получаем имя
@dp.message(RequestForm.waiting_for_name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("О чём ты хочешь поговорить на консультации?")
    await state.set_state(RequestForm.waiting_for_topic)

# 🔹 Получаем тему
@dp.message(RequestForm.waiting_for_topic)
async def get_topic(message: types.Message, state: FSMContext):
    await state.update_data(topic=message.text)
    await message.answer("Как с тобой связаться? (например, @username или телефон)")
    await state.set_state(RequestForm.waiting_for_contact)

# 🔹 Получаем контакт и отправляем заявку админу
@dp.message(RequestForm.waiting_for_contact)
async def get_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    data = await state.get_data()

    # Формируем текст заявки
    text = (
        f"📩 <b>Новая заявка на консультацию</b>\n\n"
        f"👤 Имя: {data['name']}\n"
        f"💬 Тема: {data['topic']}\n"
        f"📱 Контакт: {data['contact']}\n"
        f"🔗 Пользователь: @{message.from_user.username or 'без никнейма'}"
    )

    # Отправляем админу
    await bot.send_message(ADMIN_ID, text, parse_mode="HTML")

    await message.answer(
        "Спасибо! 🙌 Я передал заявку специалисту. Он свяжется с тобой в ближайшее время."
    )
    await state.clear()

# 🔹 Остальные сообщения
@dp.message()
async def fallback(message: types.Message):
    await message.answer("Я пока отвечаю только на вопросы о консультациях 🙂 Напиши /start, чтобы начать заново.")

# 🔹 Запуск
async def main():
    print("🤖 Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
