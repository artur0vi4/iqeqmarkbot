import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Ссылки на группы (твои 9 групп)
GROUPS = {
    "1_1": "https://t.me/+group1_spokoinoe",
    "1_2": "https://t.me/+group2_druzhelyubnye", 
    "1_3": "https://t.me/+group3_teplye",
    "2_1": "https://t.me/+group4_praktiki",
    "2_2": "https://t.me/+group5_balans", 
    "2_3": "https://t.me/+group6_garmoniya",
    "3_1": "https://t.me/+group7_analitiki",
    "3_2": "https://t.me/+group8_liderskoe",
    "3_3": "https://t.me/+group9_videnie"
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn_start = types.InlineKeyboardButton("🚀 НАЧАТЬ ТЕСТ", callback_data="start_quiz")
    markup.add(btn_start)
    
    bot.send_message(message.chat.id,
        "🎯 Добро пожаловать в IQ+EQ Знакомства!\n\n"
        "💡 Найди людей с похожим мышлением и чувствами\n\n"
        "👇 Нажми кнопку для старта:", 
        reply_markup=markup)

# Обработчик кнопки "НАЧАТЬ"
@bot.callback_query_handler(func=lambda call: call.data == "start_quiz")
def show_iq_menu(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    iq_buttons = [
        types.InlineKeyboardButton("1️⃣ IQ 70-105", callback_data="iq1"),
        types.InlineKeyboardButton("2️⃣ IQ 106-120", callback_data="iq2"), 
        types.InlineKeyboardButton("3️⃣ IQ 121+", callback_data="iq3")
    ]
    markup.add(*iq_buttons)
    
    bot.edit_message_text(
        "🧠 Шаг 1/2\n\nКакой у тебя IQ по тесту?", 
        call.message.chat.id, 
        call.message.message_id,
        reply_markup=markup
    )

# Обработчик IQ кнопок
@bot.callback_query_handler(func=lambda call: call.data.startswith('iq'))
def show_eq_menu(call):
    iq_level = call.data[2]  # iq1, iq2, iq3 → 1, 2, 3
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    eq_buttons = [
        types.InlineKeyboardButton("1️⃣ Низкий EQ", callback_data=f"eq1_{iq_level}"),
        types.InlineKeyboardButton("2️⃣ Средний EQ", callback_data=f"eq2_{iq_level}"),
        types.InlineKeyboardButton("3️⃣ Высокий EQ", callback_data=f"eq3_{iq_level}")
    ]
    markup.add(*eq_buttons)
    
    bot.edit_message_text(
        "❤️ Шаг 2/2\n\nКакой у тебя EQ по тесту?", 
        call.message.chat.id, 
        call.message.message_id,
        reply_markup=markup
    )

# Обработчик финальных кнопок (результат)
@bot.callback_query_handler(func=lambda call: call.data.startswith('eq'))
def send_group_link(call):
    _, iq, eq = call.data.split('_')  # eq1_2 → iq=1, eq=2
    
    group_key = f"{iq}_{eq}"
    group_link = GROUPS.get(group_key, "https://t.me/your_channel")
    
    markup = types.InlineKeyboardMarkup()
    btn_group = types.InlineKeyboardButton("👥 Перейти в группу", url=group_link)
    btn_again = types.InlineKeyboardButton("🔄 Пройти заново", callback_data="start_quiz")
    markup.add(btn_group, btn_again)
    
    # Матрица 3x3 для наглядности
    matrix = """
🧠💡 IQ+EQ МАТРИЦА 💡🧠

Спокойное    Дружелюбные    Теплые
Практики     • БАЛАНС •      Гармония  
Аналитики    Лидерское      ВИДЕНИЕ
    """
    
    bot.edit_message_text(
        f"🎉 Твоя группа: **{group_key}**\n\n{matrix}\n\n"
        f"✅ Переходи по ссылке ниже!", 
        call.message.chat.id, 
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown'
    )

print("🤖 Бот запущен!")
bot.infinity_polling()
