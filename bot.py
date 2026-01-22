@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn_start = types.InlineKeyboardButton("🚀 НАЧАТЬ ТЕСТ", callback_data="start_test")
    markup.add(btn_start)
    
    bot.send_message(message.chat.id, 
        "🎯 Добро пожаловать в IQ+EQ знакомства!\n\n"
        "💡 Найди людей с похожим мышлением и чувствами\n\n"
        "👇 Нажми кнопку ниже:", 
        reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "start_test")
def start_quiz(call):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("1️⃣ IQ 70-105")
    btn2 = types.KeyboardButton("2️⃣ IQ 106-120") 
    btn3 = types.KeyboardButton("3️⃣ IQ 121+")
    markup.add(btn1, btn2, btn3)
    
    user_states[call.from_user.id] = {'step': 'iq'}
    bot.edit_message_text(
        "1️⃣ Какой у тебя IQ по тесту?\n💡 Выбери диапазон:", 
        call.message.chat.id, 
        call.message.message_id,
        reply_markup=markup
    )
