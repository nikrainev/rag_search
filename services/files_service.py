import io

import pypdf
from providers.chroma_db import ChromaClient
from providers.yandex_gpt import YandexGpt
from typing import List
import csv

def on_get_new_file_message(bot, chat_id:int, mime_type:str, file_id:str, file_name:str, yandex_gpt:YandexGpt, chromadb:ChromaClient):
    if mime_type != 'application/pdf' and mime_type != 'text/csv':
        bot.send_message(chat_id, 'Я умею распознавать только PDF и CSV')
        return

    file_content = get_content_from_file(bot, mime_type, file_id)

    index_new_file(file_content, chat_id, yandex_gpt, chromadb, file_name)

    bot.send_message(chat_id, 'Отлично я получил ваш файл!')


def index_new_file(file_content:List[str], chat_id:int, yandex_gpt:YandexGpt, chromadb:ChromaClient, file_name:str):
    embeddings = yandex_gpt.get_embeddings(file_content)
    chromadb.insert_doc_with_embeddings(chat_id, embeddings, file_name)
    return

def get_content_from_file(bot, mime_type:str, file_id:str) -> List[str]:
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    if mime_type == 'application/pdf':
        return get_content_from_pdf_file(io.BytesIO(downloaded_file))

    if mime_type == 'text/csv':
        return get_content_from_csv_file(downloaded_file)

    return []


def get_content_from_pdf_file(path:io.BytesIO) -> List[str]:
    reader = pypdf.PdfReader(path)

    result = []
    for p in reader.pages:
        result.append(p.extract_text())

    return result

def get_content_from_csv_file(path:bytes) -> List[str]:
    data_str = path.decode('utf-8')
    csv_data = csv.reader(io.StringIO(data_str), delimiter=",")

    result = []
    for p in csv_data:
        result.append(str(p))

    return result