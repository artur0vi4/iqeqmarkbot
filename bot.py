import telebot
import time
from telebot import types

TOKEN = "8525835073:AAGfW3flAKC5yxQRGUR4UoH3sliXmDYvIbc"
bot = telebot.TeleBot(TOKEN)

INVITE_LINKS = {
    (1,1): "https://t.me/+LDqqCNtUqyhhYTky",  # Спокойное
    (1,2): "https://t.me/+gMgCyag5kTVkMjJi",  # Дружелюбные  
    (1,3): "https://t.me/+IIREb6E0mhxlNWFi", # Теплые
    (2,1): "https://t.me/+dCJR9OYZTEJkYWUy", # Практики
    (2,2): "https://t.me/+MuW-2xg2744xMjMy",  # Баланс
    (2,3): "https://t.me/+xrBnir7mBy5hNTBi", # Гармония
    (3,1): "https://t.me/+gWEKGjK_fjJmZTMy", # Аналитики
    (3,2): "https://t.me/+aLGHxsoyaA8xY2Yy", # Лидерское
    (3,3): "https://t.me/+oQRYwvMcjGxjZDU6"  # Видение
}

user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn_start = types.InlineKeyboardButton("🚀 НАЧАТЬ ТЕСТ", callback_data="start_test")
    markup.add(btn_start)
    
    bot.send_message(message.chat.id, 
        "🎯 Добро пожаловать в IQ+EQ знакомства!\n\n"
        "💡 Найди людей с похожим мышлением и чувствами\n\n"
        "👇 Нажми кнопку для старта:", 
        reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "start_test")
def start_quiz(call):
    # ✅ ИСПРАВЛЕНО: send_message вместо edit_message_text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("1️⃣ IQ 70-105")
    btn2 = types.KeyboardButton("2️⃣ IQ 106-120") 
    btn3 = types.KeyboardButton("3️⃣ IQ 121+")
    markup.add(btn1, btn2, btn3)
    
    user_states[call.from_user.id] = {'step': 'iq'}
    bot.send_message(call.message.chat.id,  # ← НОВОЕ
        "1️⃣ Какой у тебя IQ по тесту?\n💡 Выбери диапазон:", 
        reply_markup=markup)

# Остальной код БЕЗ ИЗМЕНЕНИЙ
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    if user_id not in user_states:
        bot.reply_to(message, "Напиши /start")
        return
    
    state = user_states[user_id]
    
    if state['step'] == 'iq':
        if "1️⃣" in message.text: iq_level = 1
        elif "2️⃣" in message.text: iq_level = 2
        elif "3️⃣" in message.text: iq_level = 3
        else: 
            bot.reply_to(message, "Выбери кнопку IQ!")
            return
        
        state['iq_level'] = iq_level
        state['step'] = 'eq'
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("1️⃣ EQ Низкий")
        btn2 = types.KeyboardButton("2️⃣ EQ Средний") 
        btn3 = types.KeyboardButton("3️⃣ EQ Высокий")
        markup.add(btn1, btn2, btn3)
        
        bot.send_message(message.chat.id, 
            "2️⃣ Какой у тебя EQ по тесту?\n💡 Выбери уровень:", 
            reply_markup=markup)
    
    elif state['step'] == 'eq':
        if "1️⃣" in message.text: eq_level = 1
        elif "2️⃣" in message.text: eq_level = 2
        elif "3️⃣" in message.text: eq_level = 3
        else: 
            bot.reply_to(message, "Выбери кнопку EQ!")
            return
        
        iq_level = state['iq_level']
        link = INVITE_LINKS[(iq_level, eq_level)]
        group_name = get_group_name(iq_level, eq_level)
        
        bot.send_message(message.chat.id, 
            f"✅ Твой профиль: IQ {'Низкий' if iq_level==1 else 'Средний' if iq_level==2 else 'Высокий'} | "
            f"EQ {'Низкий' if eq_level==1 else 'Средний' if eq_level==2 else 'Высокий'}\n\n"
            f"🎯 Группа: {group_name}\n🔗 {link}", 
            reply_markup=types.ReplyKeyboardRemove())
        
        del user_states[user_id]

def get_group_name(iq_l, eq_l):
    names = {
        (1,1): "Спокойное общение", (1,2): "Дружелюбные",
        (1,3): "Теплые связи", (2,1): "Практики",
        (2,2): "Баланс", (2,3): "Гармония",
        (3,1): "Аналитики", (3,2): "Лидерское",
        (3,3): "Видение"
    }
    return names.get((iq_l, eq_l), "Баланс")

print("🤖 IQ+EQ V2 кнопочный бот запущен!")
while True:
    try:
        bot.polling(none_stop=True)
    except:
        time.sleep(15)
