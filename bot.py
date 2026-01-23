from flask import Flask, request
import telebot
import os
import requests
from telebot import types

app = Flask(__name__)
TOKEN = "8525835073:AAGfW3flAKC5yxQRGUR4UoH3sliXmDYvIbc"
bot = telebot.TeleBot(TOKEN)

INVITE_LINKS = {
    (1,1): "https://t.me/+LDqqCNtUqyhhYTky",  # Убраны лишние пробелы
    (1,2): "https://t.me/+gMgCyag5kTVkMjJi",  
    (1,3): "https://t.me/+IIREb6E0mhxlNWFi", 
    (2,1): "https://t.me/+dCJR9OYZTEJkYWUy", 
    (2,2): "https://t.me/+MuW-2xg2744xMjMy", 
    (2,3): "https://t.me/+xrBnir7mBy5hNTBi", 
    (3,1): "https://t.me/+gWEKGjK_fjJmZTMy", 
    (3,2): "https://t.me/+aLGHxsoyaA8xY2Yy", 
    (3,3): "https://t.me/+oQRYwvMcjGxjZDU6"   # Убраны лишние пробелы
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
    print(f"Получено: '{message.text}'")
    
    if user_id not in user_states: 
        bot.reply_to(message, "👆 /start")
        return
    
    state = user_states[user_id]
    
    if state['step'] == 'iq':
        iq_map = {
            "1️⃣ IQ 70-105": 1, 
            "2️⃣ IQ 106-120": 2, 
            "3️⃣ IQ 121+": 3
        }
        iq_level = iq_map.get(message.text)
        if not iq_level: 
            bot.reply_to(message, "❌ Выбери IQ кнопку!")
            return
        
        state['iq_level'] = iq_level
        state['step'] = 'eq'
        print(f"IQ: {iq_level}")
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("1️⃣ EQ Низкий", "2️⃣ EQ Средний", "3️⃣ EQ Высокий")
        bot.send_message(message.chat.id, "❤️ EQ по тесту?", reply_markup=markup)
    
    elif state['step'] == 'eq':
        eq_map = {
            "1️⃣ EQ Низкий": 1,
            "2️⃣ EQ Средний": 2, 
            "3️⃣ EQ Высокий": 3
        }
        eq_level = eq_map.get(message.text)
        if not eq_level: 
            bot.reply_to(message, "❌ Выбери EQ кнопку!")
            return
        
        iq_level = state['iq_level']
        link = INVITE_LINKS[(iq_level, eq_level)]
        group_name = get_group_name(iq_level, eq_level)
        
        bot.send_message(message.chat.id, 
            f"🎉 ГРУППА: **{group_name}**\n🔗 {link}", 
            reply_markup=types.ReplyKeyboardRemove(),
            parse_mode='Markdown')
        print(f"Группа: {group_name}")
        del user_states[user_id]

def get_group_name(iq_l, eq_l):
    names = {
        (1,1): "Спокойное", 
        (1,2): "Дружелюбные", 
        (1,3): "Тёплое",  # Исправлено: было "Теплые", теперь "Тёплое"
        (2,1): "Практики", 
        (2,2): "Баланс", 
        (2,3): "Гармония",
        (3,1): "Аналитики", 
        (3,2): "Лидерское", 
        (3,3): "Видение"
    }
    return names.get((iq_l, eq_l), "Баланс")

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return 'OK', 200

@app.route('/')
def index():
    return "IQ+EQ Bot работает!", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    webhook_url = f"https://iqeqmarkbot.onrender.com/{TOKEN}"  # Исправлено: убраны лишние пробелы
    bot.remove_webhook()
    requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_url}")  # Исправлено: убраны лишние пробелы
    print("Webhook установлен!")
    app.run(host='0.0.0.0', port=port)
