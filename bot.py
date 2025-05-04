import telebot
from telebot import types
from telebot.types import InputFile
import os
import pickle
from io import BytesIO

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request

# Telegram token
TOKEN = '8035098335:AAFkCoMLWG24oiw-HBJHcEYRquzrIz6sGYw'
bot = telebot.TeleBot(TOKEN)

# Google Drive API настройки
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
creds = None
token_path = 'token.pickle'

# Загрузка токена
if os.path.exists(token_path):
    with open(token_path, 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret_750088686374-cse9ni1h2f2315cmfop6o5184vn4a7oh.apps.googleusercontent.com.json',
            SCOPES)
        creds = flow.run_local_server(port=0)
    with open(token_path, 'wb') as token:
        pickle.dump(creds, token)

# Инициализация Google Drive API
drive_service = build('drive', 'v3', credentials=creds)

# Функция для скачивания файла
def download_file_from_drive(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    file_io = BytesIO()
    downloader = MediaIoBaseDownload(file_io, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    file_io.seek(0)
    return file_io

# Словарь тем -> file_id
chapter_files = {
    "1.1 Кинематика": "13kE1V8CUKIrOI-VKhHydqbI3kNauWSgY",
    "1.2 Динамика": "15WpcxZ1rJNkoTL0hKa2jZMNLLquB2s6C",
    "1.3 Қысым": "10znvKLHr5SdpeTce19N3V3RyogUTnzz-",
    "1.4 Статика": "12qb8jSd-U0wwhQqc7fUAfZK0zIrzCnt_",
    "1.5 Сақталу заңдары": "1VRgyAYZOnRGazqdfkpjtTvY4YTmeeMCF",
    "2.1 МКТ": "13673B3xUfX1iy2n3wnvLLVcXuQyVOuqo",
    "2.2 Термодинамика": "1XX_9AgRTvpCKfzKcRNF-xQjGirHwSqyU",
    "3.1 Электростатика": "15CAblbjuHUkV8cLaMJYfJbwlsIL4CIcq",
    "3.2 Тұрақты ток": "1uuXVIZ7tcc0p0iY7dKnZW0xrgQRhIlQl",
    "3.3 Әртүрлі ортадағы электр тоғы": "19e9kbKeMyLc6h79H8KlTiKyiU2hBuQvU",
    "3.4 Магнетизм": "1ca4Cl32nPoDJK3xu_pIPYQE614MbDUri",
    "4.1 Механикалық тербелістер": "1bZeAUBxJu2Rih1uhBPz2O6HbAj_wkap_",
    "4.2 Айнымалы ток": "1SVgcpLEkB9uY3C24zD1K3Q9_BHtXJ8qk",
    "4.3 Толқындар": "1mmlQC21KLvUS_rh-DN90YppVM8IM4yTQ",
    "5.1 Оптика. Жарық": "1iloo_YIdIbkyAteCh8lj-qWOUJhpEaYu",
    "6.1 Салыстырмалы Теория": "1QaOAr7lzsv3R9lNjYS43mshOMAO4l_tV",
    "6.2 Квант физикасы": "11nBKeNyjLHHnDarBU7P7Afx_s69IK4Nz",
    "Тест": "1jNq0BVhIY4sCk7sU9Cg-ZYdhY6CgVnXY"
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
        file_id = chapter_files.get(topic)

        if file_id:
            file_io = download_file_from_drive(file_id)
            input_file = InputFile(file_io, file_name=f"{topic}.pdf")


            bot.send_document(call.message.chat.id, input_file, caption=f"📄 <b>{topic}</b> материалы:", parse_mode="HTML")

            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("📲 WhatsApp-қа өтіңіз!",
                                                  url="https://wa.me/+77085846268"))
            bot.send_message(call.message.chat.id, "Қосымша ақпарат үшін:", reply_markup=markup)

    elif data == "back_to_main":
        send_main_menu(call.message.chat.id)

bot.polling()
