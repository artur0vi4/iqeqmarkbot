import telebot
import os
import threading
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
    markup.add("1️⃣ IQ 70-105", "2️⃣ IQ 106-120", "3️⃣ IQ 121+")
    user_states[message.from_user.id] = {'step': 'iq'}
    bot.send_message(message.chat.id, "🧠 IQ по тесту? Выбери:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    if user_id not in user_states: return bot.reply_to(message, "👆 /start")
    
    state = user_states[user_id]
    if state['step'] == 'iq':
        iq_map = {"1️⃣": 1, "2️⃣": 2, "3️⃣": 3}
        iq_level = iq_map.get(message.text)
        if not iq_level: return bot.reply_to(message, "❌ IQ кнопку!")
        
        state['iq_level'] = iq_level
        state['step'] = 'eq'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("1️⃣ EQ Низкий", "2️⃣ EQ Средний", "3️⃣ EQ Высокий")
        return bot.send_message(message.chat.id, "❤️ EQ по тесту?", reply_markup=markup)
    
    elif state['step'] == 'eq':
        eq_map = {"1️⃣": 1, "2️⃣": 2, "3️⃣": 3}
        eq_level = eq_map.get(message.text)
        if not eq_level: return bot.reply_to(message, "❌ EQ кнопку!")
        
        iq_level = state['iq_level']
        link = INVITE_LINKS[(iq_level, eq_level)]
        group_name = get_group_name(iq_level, eq_level)
        
        bot.send_message(message.chat.id, 
            f"🎉 ГРУППА: **{group_name}**\n🔗 {link}", 
            reply_markup=types.ReplyKeyboardRemove(),
            parse_mode='Markdown')
        del user_states[user_id]

def get_group_name(iq_l, eq_l):
    names = {(1,1): "Спокойное", (1,2): "Дружелюбные", (1,3): "Теплые", 
             (2,1): "Практики", (2,2): "Баланс", (2,3): "Гармония", 
             (3,1): "Аналитики", (3,2): "Лидерское", (3,3): "Видение"}
    return names.get((iq_l, eq_l), "Баланс")

# ✅ Render Web Service фикс (2 строки!)
def keep_alive():
    import socket
    s = socket.socket()
    port = int(os.environ.get('PORT', 10000))
    s.bind(('0.0.0.0', port))  # ← Render видит порт!
    print(f"✅ Render порт {port} открыт!")
    s.listen(5)
    while True:
        s.accept()

if __name__ == '__main__':
    # Бот в фоне
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    print("🤖 Бот запущен!")
    # Render порт
    keep_alive()
