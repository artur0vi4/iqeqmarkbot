import telebot
import time
from telebot import types
import logging

TOKEN = "8525835073:AAGfW3flAKC5yxQRGUR4UoH3sliXmDYvIbc"
bot = telebot.TeleBot(TOKEN)

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Описания групп
GROUP_DESCRIPTIONS = {
    (1,1): "🌟 *Спокойное общение*\nЛюди с похожим уровнем IQ и EQ, ценящие комфорт и размеренность.",
    (1,2): "🤝 *Дружелюбные*\nДушевные люди с развитой эмпатией, создающие теплую атмосферу.",
    (1,3): "💖 *Теплые связи*\nВысокая эмоциональная интеллигентность создает глубокие искренние отношения.",
    (2,1): "🔧 *Практики*\nРациональный подход к жизни, ценящие конкретику и эффективность.",
    (2,2): "⚖️ *Баланс*\nГармония разума и чувств, стабильность и взвешенные решения.",
    (2,3): "🎭 *Гармония*\nИдеальное сочетание интеллекта и эмоциональной мудрости.",
    (3,1): "📊 *Аналитики*\nОстрый ум, стратегическое мышление, любовь к решению сложных задач.",
    (3,2): "👑 *Лидерское*\nПрирожденные лидеры с высоким интеллектом и эмоциональным интеллектом.",
    (3,3): "🔮 *Видение*\Инноваторы и провидцы, создающие будущее с глубоким пониманием людей."
}

INVITE_LINKS = {
    (1,1): "https://t.me/+LDqqCNtUqyhhYTky",
    (1,2): "https://t.me/+gMgCyag5kTVkMjJi",  
    (1,3): "https://t.me/+IIREb6E0mhxlNWFi",
    (2,1): "https://t.me/+dCJR9OYZTEJkYWUy",
    (2,2): "https://t.me/+MuW-2xg2744xMjMy",
    (2,3): "https://t.me/+xrBnir7mBy5hNTBi",
    (3,1): "https://t.me/+gWEKGjK_fjJmZTMy",
    (3,2): "https://t.me/+aLGHxsoyaA8xY2Yy",
    (3,3): "https://t.me/+oQRYwvMcjGxjZDU6"
}

user_states = {}

@bot.message_handler(commands=['start', 'restart'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username or "пользователь"
    
    logger.info(f"User {user_id} (@{username}) started bot")
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("1️⃣ Низкий (70-105)")
    btn2 = types.KeyboardButton("2️⃣ Средний (106-120)") 
    btn3 = types.KeyboardButton("3️⃣ Высокий (121+)")
    btn_info = types.KeyboardButton("📊 О группах")
    markup.add(btn1, btn2, btn3, btn_info)
    
    user_states[user_id] = {'step': 'iq'}
    
    welcome_text = (
        f"👋 Привет, {username}!\n\n"
        "🚀 *Добро пожаловать в IQ+EQ знакомства!*\n\n"
        "Здесь мы находим идеальные совпадения по уровню интеллекта и эмоционального интеллекта.\n\n"
        "1️⃣ *Какой у тебя IQ?*\n"
        "Выбери подходящий диапазон:"
    )
    
    bot.send_message(message.chat.id, welcome_text, 
                    reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['help', 'info'])
def help_command(message):
    help_text = (
        "📚 *Помощь по боту*\n\n"
        "*/start* - начать подбор группы\n"
        "*/help* - эта справка\n"
        "*/about* - о проекте\n\n"
        "Бот поможет найти группу по уровню IQ и EQ для комфортного общения.\n\n"
        "📈 *Уровни IQ:*\n"
        "• Низкий: 70-105\n"
        "• Средний: 106-120\n"
        "• Высокий: 121+\n\n"
        "❤️ *Уровни EQ:*\n"
        "• Низкий: требуется развитие\n"
        "• Средний: нормальный уровень\n"
        "• Высокий: развитая эмпатия"
    )
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['about'])
def about_command(message):
    about_text = (
        "🤖 *О проекте IQ+EQ*\n\n"
        "Мы создаем сообщества людей с похожим уровнем интеллекта и эмоционального интеллекта.\n\n"
        "🎯 *Цель:* помочь найти комфортную среду для общения, где вас понимают и ценят.\n\n"
        "💡 *Идея:* объединить людей не только по интересам, но и по когнитивным и эмоциональным особенностям.\n\n"
        "📊 *Методология:* основана на исследованиях в области психологии и социологии."
    )
    bot.send_message(message.chat.id, about_text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    username = message.from_user.username or str(user_id)
    
    if user_id not in user_states:
        if message.text == "📊 О группах":
            show_group_info(message)
            return
        bot.reply_to(message, "Напиши /start чтобы начать")
        return
    
    state = user_states[user_id]
    
    if message.text == "📊 О группах":
        show_group_info(message)
        return
    
    if state['step'] == 'iq':
        handle_iq_selection(message, user_id, username, state)
    elif state['step'] == 'eq':
        handle_eq_selection(message, user_id, username, state)

def handle_iq_selection(message, user_id, username, state):
    iq_map = {
        "1️⃣ Низкий (70-105)": 1,
        "2️⃣ Средний (106-120)": 2,
        "3️⃣ Высокий (121+)": 3
    }
    
    if message.text not in iq_map:
        bot.reply_to(message, "Пожалуйста, выбери один из вариантов кнопкой 👇")
        return
    
    iq_level = iq_map[message.text]
    state['iq_level'] = iq_level
    state['step'] = 'eq'
    
    logger.info(f"User {user_id} (@{username}) selected IQ level: {iq_level}")
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("😔 Низкий EQ")
    btn2 = types.KeyboardButton("😊 Средний EQ") 
    btn3 = types.KeyboardButton("🤗 Высокий EQ")
    btn_back = types.KeyboardButton("🔙 Назад к IQ")
    markup.add(btn1, btn2, btn3, btn_back)
    
    eq_info = (
        "2️⃣ *Какой у тебя уровень EQ?*\n\n"
        "📊 *Эмоциональный интеллект (EQ)* — это способность:\n"
        "• Распознавать свои и чужие эмоции\n"
        "• Управлять своими эмоциями\n"
        "• Эффективно общаться\n"
        "• Сопереживать другим\n\n"
        "Выбери наиболее подходящий вариант:"
    )
    
    bot.send_message(message.chat.id, eq_info, 
                    reply_markup=markup, parse_mode='Markdown')

def handle_eq_selection(message, user_id, username, state):
    if message.text == "🔙 Назад к IQ":
        state['step'] = 'iq'
        start(message)
        return
    
    eq_map = {
        "😔 Низкий EQ": 1,
        "😊 Средний EQ": 2,
        "🤗 Высокий EQ": 3
    }
    
    if message.text not in eq_map:
        bot.reply_to(message, "Пожалуйста, выбери один из вариантов кнопкой 👇")
        return
    
    eq_level = eq_map[message.text]
    iq_level = state['iq_level']
    
    logger.info(f"User {user_id} (@{username}) selected EQ level: {eq_level}. Total: IQ{iq_level}, EQ{eq_level}")
    
    # Получаем информацию о группе
    link = INVITE_LINKS[(iq_level, eq_level)]
    group_name = get_group_name(iq_level, eq_level)
    description = GROUP_DESCRIPTIONS[(iq_level, eq_level)]
    
    iq_texts = {1: "Низкий", 2: "Средний", 3: "Высокий"}
    eq_texts = {1: "Низкий", 2: "Средний", 3: "Высокий"}
    
    result_text = (
        f"✅ *Подбор завершен!*\n\n"
        f"📊 *Твой профиль:*\n"
        f"• IQ: *{iq_texts[iq_level]}*\n"
        f"• EQ: *{eq_texts[eq_level]}*\n\n"
        f"🎯 *Рекомендуемая группа:*\n"
        f"*{group_name}*\n\n"
        f"{description}\n\n"
        f"🔗 *Ссылка для вступления:*\n{link}\n\n"
        f"💡 *Совет:* Будь активным в группе, участвуй в обсуждениях!"
    )
    
    # Создаем inline-кнопку для быстрого перехода
    inline_markup = types.InlineKeyboardMarkup()
    inline_btn = types.InlineKeyboardButton("✨ Перейти в группу", url=link)
    inline_markup.add(inline_btn)
    
    bot.send_message(message.chat.id, result_text, 
                    reply_markup=inline_markup, parse_mode='Markdown')
    
    # Отправляем отдельное сообщение с предложением начать заново
    time.sleep(1)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    restart_btn = types.KeyboardButton("/start")
    markup.add(restart_btn)
    
    bot.send_message(message.chat.id, 
                    "Хочешь попробовать другие настройки? Нажми /start",
                    reply_markup=markup)
    
    del user_states[user_id]

def show_group_info(message):
    info_text = (
        "📊 *О группах IQ+EQ*\n\n"
        "Мы разделили сообщества на 9 групп, каждая со своей атмосферой:\n\n"
        "1️⃣ *Спокойное общение* - Комфорт и размеренность\n"
        "2️⃣ *Дружелюбные* - Теплая атмосфера и поддержка\n"
        "3️⃣ *Теплые связи* - Глубокие искренние отношения\n"
        "4️⃣ *Практики* - Конкретика и эффективность\n"
        "5️⃣ *Баланс* - Стабильность и гармония\n"
        "6️⃣ *Гармония* - Идеальное сочетание ума и чувств\n"
        "7️⃣ *Аналитики* - Стратегия и решение задач\n"
        "8️⃣ *Лидерское* - Прирожденные лидеры\n"
        "9️⃣ *Видение* - Инноваторы и провидцы\n\n"
        "🎯 *Цель:* найти именно ту среду, где ты будешь чувствовать себя максимально комфортно!"
    )
    bot.send_message(message.chat.id, info_text, parse_mode='Markdown')

def get_group_name(iq_l, eq_l):
    names = {
        (1,1): "Спокойное общение", (1,2): "Дружелюбные",
        (1,3): "Теплые связи", (2,1): "Практики",
        (2,2): "Баланс", (2,3): "Гармония",
        (3,1): "Аналитики", (3,2): "Лидерское",
        (3,3): "Видение"
    }
    return names.get((iq_l, eq_l), "Баланс")

# Обработка команды для администратора
@bot.message_handler(commands=['stats'])
def stats_command(message):
    # Проверяем, является ли пользователь администратором (можно добавить проверку по ID)
    admin_ids = []  # Добавь сюда ID администраторов
    
    if message.from_user.id in admin_ids or len(admin_ids) == 0:  # Если нет админов, команда доступна всем
        stats_text = (
            f"📊 *Статистика бота*\n\n"
            f"• Пользователей в процессе: {len(user_states)}\n"
            f"• Всего состояний в памяти: {len(user_states)}\n"
            f"• Бот работает стабильно ✅"
        )
        bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')
    else:
        bot.reply_to(message, "Эта команда только для администраторов")

if __name__ == "__main__":
    logger.info("🤖 IQ+EQ V3 бот запущен!")
    print("=" * 50)
    print("IQ+EQ Matchmaking Bot запущен и готов к работе!")
    print("=" * 50)
    
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=30)
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            print(f"Произошла ошибка: {e}")
            print("Перезапуск через 10 секунд...")
            time.sleep(10)
