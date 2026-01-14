import telebot
import re

TOKEN = "8525835073:AAGfW3flAKC5yxQRGUR4UoH3sliXmDYvIbc"
bot = telebot.TeleBot(TOKEN)

# ТВОИ ссылки из скрина (замени все 9):
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

@bot.message_handler(commands=['start'])
def start(message):
    text = message.text.replace('/start ', '').upper()
    iq_match = re.search(r'IQ(\d+)', text)
    eq_match = re.search(r'EQ(\d+)', text)
    
    if iq_match and eq_match:
        iq = int(iq_match.group(1))
        eq = int(eq_match.group(1))
        
        iq_level = 1 if iq <= 105 else 2 if iq <= 120 else 3
        eq_level = 1 if eq <= 65 else 2 if eq <= 90 else 3
        
        link = INVITE_LINKS.get((iq_level, eq_level), INVITE_LINKS[(2,2)])
        bot.reply_to(message, f"✅ IQ{iq} EQ{eq}\n🔗 {link}")
    else:
        bot.reply_to(message, "❌ Формат: /start IQ115EQ78")

while True:
    try:
        bot.polling(none_stop=True)
    except:
        pass
