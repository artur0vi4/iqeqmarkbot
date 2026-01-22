import telebot
import time
import requests
from telebot import types

TOKEN = "8525835073:AAGfW3flAKC5yxQRGUR4UoH3sliXmDYvIbc"
bot = telebot.TeleBot(TOKEN)

# Жестко убиваем старые процессы
def kill_old_instances():
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
        requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset=-1")
        print("✅ Старые процессы убиты!")
    except:
        pass

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
    markup = types.InlineKeyboardMarkup()
    btn_start = types.InlineKeyboardButton("🚀 НАЧАТЬ ТЕСТ", callback_data="start_test")
    markup.add(btn_start)
    bot.send_message(message.chat.id, "🎯 IQ+EQ знакомства!\n👇 Нажми:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "start_test")
def start_quiz(call):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("1️⃣ IQ 70-105", "2️⃣ IQ 106-120", "3️⃣ IQ 121+")
    user_states[call.from_user.id] = {'step': 'iq'}
    bot.send_message(call.message.chat.id, "1️⃣ IQ по тесту?", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    if user_id not in user_states: 
        bot.reply_to(message, "Напиши /start")
        return
    
    state = user_states[user_id]
    if state['step'] == 'iq':
        iq_map = {"1️⃣": 1, "2️⃣": 2, "3️⃣": 3}
        iq_level = iq_map.get(message.text)
        if not iq_level: return bot.reply_to(message, "Выбери IQ!")
        
        state['iq_level'] = iq_level
        state['step'] = 'eq'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("1️⃣ EQ Низкий", "2️⃣ EQ Средний", "3️⃣ EQ Высокий")
        return bot.send_message(message.chat.id, "2️⃣ EQ по тесту?", reply_markup=markup)
    
    elif state['step'] == 'eq':
        eq_map = {"1️⃣": 1, "2️⃣": 2, "3️⃣": 3}
        eq_level = eq_map.get(message.text)
        if not eq_level: return bot.reply_to(message, "Выбери EQ!")
        
        iq_level = state['iq_level']
        link = INVITE_LINKS[(iq_level, eq_level)]
        group_name = get_group_name(iq_level, eq_level)
        
        bot.send_message(message.chat.id, 
            f"IQ {'Низкий' if iq_level==1 else 'Средний' if iq_level==2 else 'Высокий'} | "
            f"EQ {'Низкий' if eq_level==1 else 'Средний' if eq_level==2 else 'Высокий'}\n\n"
            f"{group_name}\n{link}", 
            reply_markup=types.ReplyKeyboardRemove())
        del user_states[user_id]

def get_group_name(iq_l, eq_l):
    names = {(1,1): "Спокойное", (1,2): "Дружелюбные", (1,3): "Теплые", 
             (2,1): "Практики", (2,2): "Баланс", (2,3): "Гармония", 
             (3,1): "Аналитики", (3,2): "Лидерское", (3,3): "Видение"}
    return names.get((iq_l, eq_l), "Баланс")

# ✅ ЖЕСТКОЕ ОЧИЩЕНИЕ ПЕРЕД ЗАПУСКОМ
print("🔥 Убиваем старые боты...")
kill_old_instances()
time.sleep(5)  # Даём время Telegram

print("🤖 IQ+EQ бот запускается...")
for i in range(10):  # 10 попыток подключения
    try:
        bot.polling(none_stop=True, interval=1, timeout=10)
        break
    except Exception as e:
        print(f"Попытка {i+1}/10: {e}")
        time.sleep(10)
