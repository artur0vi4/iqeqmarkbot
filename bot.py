from telebot import types

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn_start = types.InlineKeyboardButton("🚀 Начать", callback_data="start_quiz")
    markup.add(btn_start)
    
    bot.send_message(message.chat.id, 
        "🚀 Добро пожаловать в IQ+EQ знакомства!\n\n"
        "Нажми кнопку ниже, чтобы найти свою группу:", 
        reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "start_quiz")
def start_quiz(call):
    bot.edit_message_text(
        "1️⃣ Какой у тебя IQ по тесту?\n💡 Выбери диапазон:", 
        call.message.chat.id, 
        call.message.message_id,
        reply_markup=get_iq_keyboard()
    )

def get_iq_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("1️⃣ IQ 70-105", "2️⃣ IQ 106-120", "3️⃣ IQ 121+")
    return markup
