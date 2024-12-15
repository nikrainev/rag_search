from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk._types.model import BaseModel

from providers.config import get_config
from typing import List
from typing import Dict

SYSTEM_PROMPT = ("Ты специалист технической поддежки. "
                 "На основе сообщений, написанных тобой выше, сгенерируй сообщение")

class YandexGpt:
    def __init__(self):
        config = get_config()
        self.sdk = YCloudML(folder_id=config['yandex_ml_folder_id'], auth=config['yandex_API_token'])

    def get_item_emdeddings(self, text: str) -> tuple:
        doc_model = self.sdk.models.text_embeddings('doc')
        doc_embeddings = doc_model.run(text)

        return doc_embeddings[:]

    def get_embeddings(self, doc_texts: List[str]) -> List[Dict]:
        result = []

        for t in doc_texts:
            result.append({
                'text': t,
                'text_embeddings': []
            })

        text_embeddings = []
        for txt in result:
            text_embeddings.append(self.get_item_emdeddings(txt['text']))
            txt["text_embeddings"] = list(text_embeddings[0])

        return result

    def get_completion_model(self) -> BaseModel:
        model = self.sdk.models.completions('yandexgpt')
        model = model.configure(temperature=0.5)
        return model


# %%
