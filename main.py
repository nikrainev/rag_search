from providers.yandex_gpt import YandexGpt
from providers.chroma_db import ChromaClient
import telebot
from providers.config import get_config
from services.files_service import  on_get_new_file_message
from services.requests_service import perform_user_query, list_indexed_files

yandexGpt = YandexGpt()
chroma_client = ChromaClient()

config = get_config()
bot=telebot.TeleBot(config.get('bot_token'))

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Привет ✌️ . Отправьте мне файлы в формате PDF или CSV (с помощью функции прикрепить документ), и я полностью их изучу. Для поиска по файлам просто отправьте текстовое сообщение с вопросом. Для просмотра списка проиндексированных файлов отправьте /list_docs")
    pass

@bot.message_handler(commands=['list_docs'])
def list_files(message):
    result = list_indexed_files(message.chat.id, chroma_client)
    bot.send_message(message.chat.id, result)
    pass

@bot.message_handler(content_types=['document'])
def doc_message(message):
    on_get_new_file_message(bot, message.chat.id, message.document.mime_type, message.document.file_id, message.document.file_name, yandexGpt, chroma_client)
    pass

@bot.message_handler(func=lambda message: True)
def text_message(message):
    if  message.text != '/list_docs':
        result = perform_user_query(message.chat.id, message.text, yandexGpt, chroma_client)
        bot.send_message(message.chat.id, result)
    pass


bot.infinity_polling()