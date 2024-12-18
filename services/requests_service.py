from __future__ import annotations

from providers.chroma_db import ChromaClient
from providers.yandex_gpt import YandexGpt
from providers.admin_api import send_create_user_request


def perform_user_query(chat_id: int, text_query: str, yandex_gpt: YandexGpt, chromadb: ChromaClient) -> str:
    user_collection = chromadb.get_or_create_collection(chat_id)
    embeddings = yandex_gpt.get_item_emdeddings(text_query)
    completion_model = yandex_gpt.get_completion_model()

    result = user_collection.query(
        query_embeddings=list(embeddings),
        n_results=6,
    )

    messages: list[dict[str, str] | str] = [
        {'role': 'system', 'text': 'Не отвечай на вопросы ответ на которые нельзя получить в эмбедингах '}]

    for distance, metadata, document in zip(
            result["distances"][0], result["metadatas"][0], result["documents"][0]
    ):
        if distance < 1:
            messages.append({'role': 'user', 'text': metadata["text"]})
            messages.append({'role': 'assistant', 'text': document})

    messages.append({'role': 'user', 'text': text_query})

    result = completion_model.run(messages)
    messages.append(result[0])

    send_create_user_request(chat_id, requestText=text_query, responseText=result[0].text)

    return result[0].text


def list_indexed_files(chat_id: int, chromadb: ChromaClient) -> str:
    result = chromadb.get_collection_metadata(chat_id)
    return str(set(result))
