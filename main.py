import telebot
import random
from telebot import types
from config import BOT_TOKEN  # Импортируем токен from config

# Создаем экземпляр бота
bot = telebot.TeleBot(BOT_TOKEN)

# Списки мотивирующих фраз
MOTIVATIONS = [
    "Сегодня твой день — начни его с улыбки!",
    "Ты намного сильнее, чем думаешь.",
    "Каждый шаг вперед — это победа над вчерашним собой.",
    "Успех начинается с первого шага. Сделай его прямо сейчас!",
    "Твои возможности безграничны — верь в себя!",
    "Не бойся мечтать больше, чем кажется возможным.",
    "Сегодня — идеальный день для достижения целей.",
    "Ты можешь больше, чем думаешь, и умеешь больше, чем знаешь.",
    "Каждая неудача — это урок на пути к успеху.",
    "Твоя решимость сильнее любых препятствий.",
    "Начни с малого, но начни сегодня!",
    "Ты автор своей истории — сделай её вдохновляющей!",
    "Прогресс важнее совершенства.",
    "Твоя цель ближе, чем кажется — продолжай идти!",
    "Сегодня ты можешь стать лучше, чем вчера."
]

# Списки мотивирующих цитат
SMART_QUOTES = [
    "Секрет перемен состоит в том, чтобы сосредоточиться на создании нового, а не на борьбе со старым. — Сократ, древнегреческий философ.",
    "Единственный способ делать великие дела — это любить то, что ты делаешь. — Стив Джобс, основатель Apple.",
    "Будь собой, все остальные роли уже заняты. — Оскар Уайльд, писатель.",
    "Жизнь — это то, что с тобой происходит, пока ты строишь другие планы. — Джон Леннон, музыкант.",
    "Успех — это способность идти от одной неудачи к другой, не теряя энтузиазма. — Уинстон Черчилль, политик.",
    "Не важно, насколько медленно ты идешь, главное — не останавливаться. — Конфуций, философ.",
    "Будущее принадлежит тем, кто верит в красоту своих мечтаний. — Элеонора Рузвельт, политик.",
    "Образование — самое мощное оружие, которое можно использовать, чтобы изменить мир. — Нельсон Мандела, политик.",
    "Путь в тысячу миль начинается с одного шага. — Лао-цзы, философ.",
    "Мы становимся тем, о чем думаем. — Эрл Найтингейл, писатель.",
    "Жизнь — это 10% того, что происходит с тобой, и 90% того, как ты на это реагируешь. — Чарльз Суиндолл, писатель.",
    "Не жди идеального момента, сделай момент идеальным. — Зориг Ринпоче, учитель.",
    "Лучшее время посадить дерево было 20 лет назад. Второе лучшее время — сейчас. — Китайская пословица.",
    "Невозможно — это не факт, а мнение. — Мухаммед Али, боксер.",
    "Твоя жизнь не улучшается случайно, она улучшается благодаря изменениям. — Джим Рон, мотивационный спикер."
]

# Стандартный ответ для неизвестных команд
STANDARD_RESPONSE = "Введи `/getmotivation` для получения мотивирующей фразы или `/getsmartquote` для получения мотивирующей цитаты."


def create_motivation_keyboard():
    """Создание inline-клавиатуры с кнопками мотивации"""
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    btn_motivation = types.InlineKeyboardButton(
        text="✨ Получить мотивирующую фразу",
        callback_data="get_motivation"
    )
    btn_quote = types.InlineKeyboardButton(
        text="💡 Получить мотивирующую цитату",
        callback_data="get_quote"
    )

    keyboard.add(btn_motivation, btn_quote)
    return keyboard


@bot.message_handler(commands=['start'])
def start_message(message):
    """Обработчик команды /start"""
    welcome_text = f"""
👋 Привет, {message.from_user.first_name}!

Я — твой личный бот-мотиватор! 🚀

🌟 Мои возможности:
• Мотивирующие фразы для поднятия настроения
• Мудрые цитаты великих людей

Готов зарядить тебя позитивом? Выбери нужную опцию! 💪
"""
    keyboard = create_motivation_keyboard()
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)


@bot.message_handler(commands=['getmotivation'])
def get_motivation(message):
    """Обработчик команды /getmotivation"""
    motivation = random.choice(MOTIVATIONS)
    keyboard = create_motivation_keyboard()
    bot.send_message(message.chat.id, f"✨ {motivation}", reply_markup=keyboard)


@bot.message_handler(commands=['getsmartquote'])
def get_smart_quote(message):
    """Обработчик команды /getsmartquote"""
    quote = random.choice(SMART_QUOTES)
    keyboard = create_motivation_keyboard()
    bot.send_message(message.chat.id, f"💡 {quote}", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    """Обработчик нажатий на inline-кнопки"""
    try:
        if call.data == "get_motivation":
            motivation = random.choice(MOTIVATIONS)
            keyboard = create_motivation_keyboard()
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"✨ {motivation}",
                reply_markup=keyboard
            )
        elif call.data == "get_quote":
            quote = random.choice(SMART_QUOTES)
            keyboard = create_motivation_keyboard()
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"💡 {quote}",
                reply_markup=keyboard
            )

        # Отвечаем на callback, чтобы убрать "загрузку" с кнопки
        bot.answer_callback_query(call.id)

    except Exception as e:
        print(f"Ошибка в callback: {e}")
        bot.answer_callback_query(call.id, "Произошла ошибка, попробуй еще раз")


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Обработчик всех остальных сообщений"""
    keyboard = create_motivation_keyboard()
    bot.send_message(message.chat.id, STANDARD_RESPONSE, reply_markup=keyboard)


# Запуск бота
if __name__ == "__main__":
    print("🤖 Бот запущен...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"❌ Ошибка: {e}")


