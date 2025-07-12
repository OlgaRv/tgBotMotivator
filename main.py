import random, logging
import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    CallbackContext
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Создание логгера для текущего модуля
logger = logging.getLogger(__name__)

# Настройка системы логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Мотивационные фразы
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

# Мудрые цитаты
SMART_QUOTES = [
    "Секрет перемен состоит в том, чтобы сосредоточиться на создании нового, а не на борьбе со старым. — Сократ",
    "Единственный способ делать великие дела — это любить то, что ты делаешь. — Стив Джобс",
    "Будь собой, все остальные роли уже заняты. — Оскар Уайльд",
    "Жизнь — это то, что с тобой происходит, пока ты строишь другие планы. — Джон Леннон",
    "Успех — это способность идти от одной неудачи к другой, не теряя энтузиазма. — Уинстон Черчилль",
    "Не важно, насколько медленно ты идешь, главное — не останавливаться. — Конфуций",
    "Будущее принадлежит тем, кто верит в красоту своих мечтаний. — Элеонора Рузвельт",
    "Образование — самое мощное оружие, которое можно использовать, чтобы изменить мир. — Нельсон Мандела",
    "Путь в тысячу миль начинается с одного шага. — Лао-цзы",
    "Мы становимся тем, о чём думаем. — Эрл Найтингейл",
    "Жизнь — это 10% того, что происходит с тобой, и 90% того, как ты на это реагируешь. — Чарльз Суиндолл",
    "Не жди идеального момента, сделай момент идеальным. — Зориг Ринпоче",
    "Лучшее время посадить дерево было 20 лет назад. Второе лучшее — сейчас. — Китайская пословица",
    "Невозможно — это не факт, а мнение. — Мухаммед Али",
    "Твоя жизнь не улучшается случайно, она улучшается благодаря изменениям. — Джим Рон"
]


def create_keyboard():
    """Создает основную клавиатуру с кнопками действий"""
    keyboard = [
        [InlineKeyboardButton("✨ Получить мотивацию", callback_data='get_motivation')],
        [InlineKeyboardButton("💡 Получить цитату", callback_data='get_quote')],
        [InlineKeyboardButton("❌ Выйти", callback_data='exit')]
    ]
    return InlineKeyboardMarkup(keyboard)


def create_exit_confirmation_keyboard():
    """Создает клавиатуру подтверждения выхода"""
    keyboard = [
        [InlineKeyboardButton("✅ Да, выйти", callback_data='confirm_exit')],
        [InlineKeyboardButton("❌ Нет, остаться", callback_data='cancel_exit')]
    ]
    return InlineKeyboardMarkup(keyboard)


# /start
def start(update: Update, context: CallbackContext):
    name = update.effective_user.first_name
    text = f"""👋 Привет, {name}!

Я — твой личный бот-мотиватор! 🚀

🌟 Мои возможности:
• Мотивирующие фразы
• Мудрые цитаты

Готов зарядиться позитивом? Выбирай кнопку ниже! 💪"""
    update.message.reply_text(text, reply_markup=create_keyboard())


# /getmotivation
def get_motivation(update: Update, context: CallbackContext):
    motivation = random.choice(MOTIVATIONS)
    update.message.reply_text(f"✨ {motivation}", reply_markup=create_keyboard())


# /getsmartquote
def get_smart_quote(update: Update, context: CallbackContext):
    quote = random.choice(SMART_QUOTES)
    update.message.reply_text(f"💡 {quote}", reply_markup=create_keyboard())


# /exit - команда для выхода
def exit_command(update: Update, context: CallbackContext):
    text = "Вы уверены, что хотите выйти? 🤔"
    update.message.reply_text(text, reply_markup=create_exit_confirmation_keyboard())


# Inline-кнопки
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "get_motivation":
        text = f"✨ {random.choice(MOTIVATIONS)}"
        query.edit_message_text(text=text, reply_markup=create_keyboard())

    elif query.data == "get_quote":
        text = f"💡 {random.choice(SMART_QUOTES)}"
        query.edit_message_text(text=text, reply_markup=create_keyboard())

    elif query.data == "exit":
        text = "Вы уверены, что хотите выйти? 🤔"
        query.edit_message_text(text=text, reply_markup=create_exit_confirmation_keyboard())

    elif query.data == "confirm_exit":
        text = """👋 До свидания!

Было приятно мотивировать вас! 😊
Если захотите вернуться, просто напишите /start

Удачи во всех начинаниях! 🌟"""
        query.edit_message_text(text=text)

    elif query.data == "cancel_exit":
        name = query.from_user.first_name
        text = f"Отлично, {name}! Продолжаем мотивироваться! 💪"
        query.edit_message_text(text=text, reply_markup=create_keyboard())

    else:
        text = "Неизвестная команда."
        query.edit_message_text(text=text, reply_markup=create_keyboard())


# Ответ на любое другое сообщение
def unknown_message(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Введи /getmotivation, /getsmartquote, /exit или нажми кнопку ниже 👇",
        reply_markup=create_keyboard()
    )


# Запуск
def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    # Команды
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("getmotivation", get_motivation))
    dp.add_handler(CommandHandler("getsmartquote", get_smart_quote))
    dp.add_handler(CommandHandler("exit", exit_command))

    # Inline-кнопки
    dp.add_handler(CallbackQueryHandler(button_handler))

    # Все остальные сообщения
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, unknown_message))

    print("🤖 Бот запущен...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()