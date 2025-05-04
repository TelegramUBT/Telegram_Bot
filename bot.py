import telebot
from telebot import types
from telebot.types import InputFile
import os

# Telegram token
TOKEN = '8035098335:AAFkCoMLWG24oiw-HBJHcEYRquzrIz6sGYw'
bot = telebot.TeleBot(TOKEN)

# Словарь тем -> имена файлов
chapter_files = {
    "1.1 Кинематика": "1.1.Кинематика.pdf",
    "1.2 Динамика": "1.2.Динамика.pdf",
    "1.3 Қысым": "1.3.Кысым.pdf",
    "1.4 Статика": "1.4.Статика.pdf",
    "1.5 Сақталу заңдары": "1.5.Сакталу зандары.pdf",
    "2.1 МКТ": "2.1. МКТ.pdf",
    "2.2 Термодинамика": "2.2.Термодинамика.pdf",
    "3.1 Электростатика": "3.1.Электростатика.pdf",
    "3.2 Тұрақты ток": "3.2 Туракты ток.pdf",
    "3.3 Әртүрлі ортадағы электр тоғы": "3.3.Артурли ортадагы электр тогы.pdf",
    "3.4 Магнетизм": "3.4. Магнетизм.pdf",
    "4.1 Механикалық тербелістер": "4.1. Механикалык тербелистер.pdf",
    "4.2 Айнымалы ток": "4.2. Айнымалы ток.pdf",
    "4.3 Толқындар": "4.3. Толкындар.pdf",
    "5.1 Оптика. Жарық": "5.1. Оптика. Жарык.pdf",
    "6.1 Салыстырмалы Теория": "6.1. Салыстырмалы теория.pdf",
    "6.2 Квант физикасы": "6.2. Квант Физикасы.pdf",
    "Тест": "Тест.pdf"
}

# Разделы
subsections = {
    "section_1": ["1.1 Кинематика", "1.2 Динамика", "1.3 Қысым", "1.4 Статика", "1.5 Сақталу заңдары"],
    "section_2": ["2.1 МКТ", "2.2 Термодинамика"],
    "section_3": ["3.1 Электростатика", "3.2 Тұрақты ток", "3.3 Әртүрлі ортадағы электр тоғы", "3.4 Магнетизм"],
    "section_4": ["4.1 Механикалық тербелістер", "4.2 Айнымалы ток", "4.3 Толқындар"],
    "section_5": ["5.1 Оптика. Жарық"],
    "section_6": ["6.1 Салыстырмалы Теория", "6.2 Квант физикасы"],
    "section_7": ["Тест"]
}

# Главное меню
def send_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("1 бөлім: Механика", callback_data="section_1"),
        types.InlineKeyboardButton("2 бөлім: Жылу физикасы", callback_data="section_2"),
        types.InlineKeyboardButton("3 бөлім: Электр және магнетизм", callback_data="section_3"),
        types.InlineKeyboardButton("4 бөлім: Тербелістер. Толқындар", callback_data="section_4"),
        types.InlineKeyboardButton("5 бөлім: Оптика", callback_data="section_5"),
        types.InlineKeyboardButton("6 бөлім: Квант және атом физикасы", callback_data="section_6"),
        types.InlineKeyboardButton("7 бөлім: Тест сұрақтары", callback_data="section_7")
    )
    bot.send_message(chat_id,
                     "📘Сәлем жас түлек! Физика пәні бойынша өз бетімен дайындалуға арналған электрондық, әдістемелік құралға қош келдің! Физика бөлімін таңдаңыз:",
                     reply_markup=markup)

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    send_main_menu(message.chat.id)

# Обработка нажатий
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    data = call.data

    if data.startswith("section_"):
        topics = subsections.get(data, [])
        markup = types.InlineKeyboardMarkup(row_width=1)
        for topic in topics:
            markup.add(types.InlineKeyboardButton(topic, callback_data=f"sub_{topic}"))
        markup.add(types.InlineKeyboardButton("🔙 Артқа", callback_data="back_to_main"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="📂 Тақырыпты таңдаңыз:", reply_markup=markup)

    elif data.startswith("sub_"):
        topic = data[4:]
        file_name = chapter_files.get(topic)

        if file_name and os.path.exists(f"files/{file_name}"):
            file_path = f"files/{file_name}"
            input_file = InputFile(open(file_path, 'rb'))

            bot.send_document(call.message.chat.id, input_file, caption=f"📄 <b>{topic}</b> материалы:", parse_mode="HTML")

            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("📲 WhatsApp-қа өтіңіз!", url="https://wa.me/+77085170892"))
            bot.send_message(call.message.chat.id, "Қосымша ақпарат үшін:", reply_markup=markup)

    elif data == "back_to_main":
        send_main_menu(call.message.chat.id)

bot.polling()
