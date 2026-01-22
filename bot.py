import telebot
import time
from telebot import types

TOKEN = "8525835073:AAGfW3flAKC5yxQRGUR4UoH3sliXmDYvIbc"
bot = telebot.TeleBot(TOKEN)

INVITE_LINKS = {
    (1,1): "https://t.me/+LDqqCNtUqyhhYTky", (1,2): "https://t.me/+gMgCyag5kTVkMjJi", 
    (1,3): "https://t.me/+IIREb6E0mhxlNWFi", (2,1): "https://t.me/+dCJR9OYZTEJkYWUy", 
    (2,2): "https://t.me/+MuW-2xg2744xMjMy", (2,3): "https://t.me/+xrBnir7mBy5hNTBi", 
    (3,1): "https://t.me/+gWEKGjK_fjJmZTMy", (3,2): "https://t.me/+aLGHxsoyaA8xY2Yy", 
    (3,3): "https://t.me/+oQRYwvMcjGxjZDU6"
}

user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("1️⃣ IQ 70-105")
    btn2 = types.KeyboardButton("2️⃣ IQ 106-120")
    btn3 = types.KeyboardButton("3️⃣ IQ 121+")
    markup.add(btn1, btn2, btn3)
    
    user_states[message.from_user.id] = {'step': 'iq'}
    bot.send_message(message.chat.id, 
        "🧠 Шаг 1/2\n\nКакой у тебя IQ по тесту?\n💡 Выбери диапазон:", 
        reply_markup=markup)
    print(f"✅ Шаг 1: Показаны IQ кнопки для {message.from_user.id}")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    print(f"📨 Получено: '{message.text}' от {user_id}")
    
    if user_id not in user_states:
        bot.reply_to(message, "👆 Нажми /start")
        return
    
    state = user_states[user_id]
    print(f"Состояние: {state}")
    
    if state['step'] == 'iq':
        if "1️⃣" in message.text: iq_level = 1
        elif "2️⃣" in message.text: iq_level = 2
        elif "3️⃣" in message.text: iq_level = 3
        else: 
            bot.reply_to(message, "❌ Выбери кнопку IQ!")
            return
        
        state['iq_level'] = iq_level
        state['step'] = 'eq'
        print(f"✅ IQ выбран: {iq_level}")
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("1️⃣ EQ Низкий")
        btn2 = types.KeyboardButton("2️⃣ EQ Средний")
        btn3 = types.KeyboardButton("3️⃣ EQ Высокий")
        markup.add(btn1, btn2, btn3)
        
        bot.send_message(message.chat.id, 
            "❤️ Шаг 2/2\n\nКакой у тебя EQ по тесту?\n💡 Выбери уровень:", 
            reply_markup=markup)
    
    elif state['step'] == 'eq':
        if "1️⃣" in message.text: eq_level = 1
        elif "2️⃣" in message.text: eq_level = 2
        elif "3️⃣" in message.text: eq_level = 3
        else: 
            bot.reply_to(message, "❌ Выбери кнопку EQ!")
            return
        
        iq_level = state['iq_level']
        link = INVITE_LINKS[(iq_level, eq_level)]
        group_name = get_group_name(iq_level, eq_level)
        
        iq_text = 'Низкий (70-105)' if iq_level==1 else 'Средний (106-120)' if iq_level==2 else 'Высокий (121+)'
        eq_text = 'Низкий' if eq_level==1 else 'Средний' if eq_level==2 else 'Высокий'
        
        bot.send_message(message.chat.id, 
            f"🎉 ТВОЯ ГРУППА НАЙДЕНА!\n\n"
            f"🧠 IQ: {iq_text}\n"
            f"❤️ EQ: {eq_text}\n\n"
            f"👥 Группа: **{group_name}**\n"
            f"🔗 {link}\n\n"
            f"✅ Переходи и знакомься!", 
            reply_markup=types.ReplyKeyboardRemove(),
            parse_mode='Markdown')
        
        print(f"✅ Шаг 4: Группа {group_name} для {user_id}")
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

print("🤖 IQ+EQ бот запущен!")
bot.infinity_polling()
