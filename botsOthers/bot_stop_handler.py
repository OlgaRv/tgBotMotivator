import random
import sys
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler
)
from config import BOT_TOKEN  # Убедись, что в config.py есть переменная BOT_TOKEN

# ID администратора бота (замените на свой Telegram ID для безопасности)
ADMIN_ID = None  # Установите свой ID, например: ADMIN_ID = 123456789

# Состояния для ConversationHandler
CONFIRM_STOP = 1

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

# Глобальная переменная для хранения updater
updater = None


def create_keyboard():
    keyboard = [
        [InlineKeyboardButton("✨ Получить мотивацию", callback_data='get_motivation')],
        [InlineKeyboardButton("💡 Получить цитату", callback_data='get_quote')],
        [InlineKeyboardButton("🛑 Остановить бота", callback_data='stop_bot')]
    ]
    return InlineKeyboardMarkup(keyboard)


def create_confirmation_keyboard():
    keyboard = [
        [InlineKeyboardButton("✅ Да, остановить", callback_data='confirm_stop')],
        [InlineKeyboardButton("❌ Нет, продолжить", callback_data='cancel_stop')]
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
• Возможность остановки бота командой /stop

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


# === ConversationHandler функции для остановки ===

def start_stop_conversation(update: Update, context: CallbackContext):
    """Начало разговора об остановке бота"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    # Проверка прав администратора (опционально)
    if ADMIN_ID is not None and user_id != ADMIN_ID:
        if update.message:
            update.message.reply_text("❌ У вас нет прав для остановки бота.")
        else:
            update.callback_query.answer("❌ У вас нет прав для остановки бота.")
        return ConversationHandler.END

    text = f"⚠️ {user_name}, вы действительно хотите остановить бота?\n\n" \
           f"🤖 Бот полностью прекратит работу и перестанет отвечать всем пользователям.\n\n" \
           f"💭 Подумайте еще раз — возможно, стоит просто закрыть чат?"

    # Обработка как команды, так и callback
    if update.message:
        update.message.reply_text(text, reply_markup=create_confirmation_keyboard())
    else:
        query = update.callback_query
        query.answer()
        query.edit_message_text(text=text, reply_markup=create_confirmation_keyboard())

    return CONFIRM_STOP


def confirm_stop(update: Update, context: CallbackContext):
    """Подтверждение остановки бота"""
    query = update.callback_query
    query.answer()

    user_name = update.effective_user.first_name
    user_id = update.effective_user.id

    if query.data == 'confirm_stop':
        goodbye_text = f"👋 До свидания, {user_name}!\n\n" \
                       f"🤖 Бот остановлен по вашей команде.\n\n" \
                       f"💙 Спасибо за использование! До новых встреч!"

        query.edit_message_text(text=goodbye_text)

        print(f"🛑 Бот остановлен пользователем {user_name} (ID: {user_id})")

        # Остановка бота
        if updater:
            updater.stop()
            updater.is_idle = False

        # Завершение программы
        os._exit(0)

    elif query.data == 'cancel_stop':
        text = f"😊 Отлично, {user_name}! Бот продолжает работу.\n\n" \
               f"Что будем делать дальше?"

        query.edit_message_text(text=text, reply_markup=create_keyboard())

    return ConversationHandler.END


def cancel_stop(update: Update, context: CallbackContext):
    """Отмена разговора об остановке"""
    user_name = update.effective_user.first_name
    text = f"😊 Отлично, {user_name}! Бот продолжает работу.\n\n" \
           f"Что будем делать дальше?"

    update.message.reply_text(text, reply_markup=create_keyboard())
    return ConversationHandler.END


# Обработка неправильного ввода во время разговора
def wrong_input_in_conversation(update: Update, context: CallbackContext):
    """Обработка неправильного ввода в разговоре"""
    text = "🤔 Пожалуйста, используйте кнопки для ответа.\n\n" \
           "✅ Да, остановить — если хотите остановить бота\n" \
           "❌ Нет, продолжить — если хотите продолжить работу\n\n" \
           "Или отправьте /cancel для отмены."

    update.message.reply_text(text, reply_markup=create_confirmation_keyboard())
    return CONFIRM_STOP


# === Обычные inline-кнопки ===

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query

    # Если это кнопки подтверждения остановки, не обрабатываем их здесь
    if query.data in ['confirm_stop', 'cancel_stop']:
        return

    query.answer()

    if query.data == "get_motivation":
        text = f"✨ {random.choice(MOTIVATIONS)}"
        query.edit_message_text(text=text, reply_markup=create_keyboard())
    elif query.data == "get_quote":
        text = f"💡 {random.choice(SMART_QUOTES)}"
        query.edit_message_text(text=text, reply_markup=create_keyboard())
    elif query.data == "stop_bot":
        # Запуск разговора об остановке
        start_stop_conversation(update, context)
    else:
        text = "Неизвестная команда."
        query.edit_message_text(text=text, reply_markup=create_keyboard())


# Ответ на любое другое сообщение
def unknown_message(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Введи /getmotivation, /getsmartquote, /stop или нажми кнопку ниже 👇",
        reply_markup=create_keyboard()
    )


# Запуск
def main():
    global updater

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # ConversationHandler для остановки бота
    stop_conversation = ConversationHandler(
        entry_points=[
            CommandHandler('stop', start_stop_conversation),
            CallbackQueryHandler(start_stop_conversation, pattern='^stop_bot$')
        ],
        states={
            CONFIRM_STOP: [
                CallbackQueryHandler(confirm_stop, pattern='^(confirm_stop|cancel_stop)$'),
                MessageHandler(Filters.text & ~Filters.command, wrong_input_in_conversation)
            ]
        },
        fallbacks=[
            CommandHandler('cancel', cancel_stop),
            MessageHandler(Filters.command, cancel_stop)
        ]
    )

    # Добавляем обработчики
    dp.add_handler(stop_conversation)

    # Обычные команды
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("getmotivation", get_motivation))
    dp.add_handler(CommandHandler("getsmartquote", get_smart_quote))

    # Inline-кнопки
    dp.add_handler(CallbackQueryHandler(button_handler))

    # Все остальные сообщения
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, unknown_message))

    print("🤖 Бот запущен...")

    try:
        updater.start_polling()
        updater.idle()
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен через Ctrl+C")
        updater.stop()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()