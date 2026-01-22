@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    if user_id not in user_states: return bot.reply_to(message, "👆 /start")
    
    state = user_states[user_id]
    if state['step'] == 'iq':
        # ✅ ФИКС: точное сравнение текста кнопок
        iq_map = {
            "1️⃣ IQ 70-105": 1, 
            "2️⃣ IQ 106-120": 2, 
            "3️⃣ IQ 121+": 3
        }
        iq_level = iq_map.get(message.text)
        if not iq_level: return bot.reply_to(message, "❌ Выбери IQ кнопку!")
        
        state['iq_level'] = iq_level
        state['step'] = 'eq'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("1️⃣ EQ Низкий", "2️⃣ EQ Средний", "3️⃣ EQ Высокий")
        return bot.send_message(message.chat.id, "❤️ EQ по тесту?", reply_markup=markup)
    
    elif state['step'] == 'eq':
        # ✅ ФИКС: точное сравнение EQ кнопок
        eq_map = {
            "1️⃣ EQ Низкий": 1,
            "2️⃣ EQ Средний": 2, 
            "3️⃣ EQ Высокий": 3
        }
        eq_level = eq_map.get(message.text)
        if not eq_level: return bot.reply_to(message, "❌ Выбери EQ кнопку!")
        
        iq_level = state['iq_level']
        link = INVITE_LINKS[(iq_level, eq_level)]
        group_name = get_group_name(iq_level, eq_level)
        
        bot.send_message(message.chat.id, 
            f"🎉 ГРУППА: **{group_name}**\n🔗 {link}", 
            reply_markup=types.ReplyKeyboardRemove(),
            parse_mode='Markdown')
        del user_states[user_id]
