import telebot
import re
import time

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
    user_states[message.from_user.id] = {'step': 1, 'iq': None}
    bot.reply_to(message, 
        "Привет! Для распределения по IQ+EQ:\n\n"
        "1️⃣ Какой у тебя результат IQ? (пиши число)\n"
        "💡 Пример: 115")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    if user_id not in user_states:
        bot.reply_to(message, "Напиши /start")
        return
    
    state = user_states[user_id]
    
    if state['step'] == 1:  # Ждём IQ
        try:
            iq = int(message.text)
            state['iq'] = iq
            state['step'] = 2
            bot.reply_to(message, f"Отлично! IQ = {iq}\n\n2️⃣ Какой результат EQ? (пиши число)")
        except:
            bot.reply_to(message, "❌ Пиши ЧИСЛО для IQ\nПример: 115")
    
    elif state['step'] == 2:  # Ждём EQ
        try:
            eq = int(message.text)
            iq = state['iq']
            
            iq_level = 1 if iq <= 105 else 2 if iq <= 120 else 3
            eq_level = 1 if eq <= 65 else 2 if eq <= 90 else 3
            
            link = INVITE_LINKS.get((iq_level, eq_level), INVITE_LINKS[(2,2)])
            group_name = get_group_name(iq_level, eq_level)
            
            bot.reply_to(message, 
                f"✅ Твой профиль: IQ {iq} | EQ {eq}\n"
                f"🎯 Группа: {group_name}\n"
                f"🔗 {link}")
            
            del user_states[user_id]
        except:
            bot.reply_to(message, "❌ Пиши ЧИСЛО для EQ")

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
while True:
    try:
        bot.polling(none_stop=True)
    except:
        time.sleep(15)
