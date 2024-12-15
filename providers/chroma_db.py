import chromadb
from chromadb.api.types import IncludeEnum
from chromadb.config import Settings
from providers.config import get_config
import ast
import string
import random
from typing import List

def id_generator(size=6, chars=string.ascii_uppercase + string.digits): return ''.join(random.choice(chars) for _ in range(size))

class ChromaClient:
    def __init__(self):
        config = get_config()
        self.chroma = chromadb.HttpClient(host=config.get('chroma_host'),
                            port=config.get('chroma_port'),
                            settings=Settings(
                                chroma_client_auth_provider="chromadb.auth.basic_authn.BasicAuthClientProvider",
                                chroma_client_auth_credentials=config.get('chroma_auth_creds')
                            ))

        self.chroma.get_or_create_collection("intents")
        self.chroma.heartbeat()
    chroma = {}

    def insert_doc_with_embeddings(self, chat_id:int, data, file_name:str):
        collection = self.chroma.get_or_create_collection('user_'+str(chat_id))

        texts = []
        text_embeddings = []
        ids = []

        for d in data:
            texts.append(d['text'])
            text_embeddings.append(d['text_embeddings'])
            ids.append(str(id_generator(10)))

        text_embeddings = list(map(
            lambda str_arr: ast.literal_eval(str(str_arr)),
            text_embeddings))

        collection.upsert(
            ids=ids,
            embeddings=text_embeddings,
            metadatas=[{"source": file_name, "text": txt} for txt in texts],
            documents=texts
        )

        return

    def get_or_create_collection(self, chat_id:int) -> chromadb.Collection:
        return self.chroma.get_or_create_collection('user_'+str(chat_id))

    def get_collection_metadata(self, chat_id:int) -> List[str]:
        collection = self.chroma.get_or_create_collection('user_'+str(chat_id))
        result = collection.get(include=[IncludeEnum.metadatas])

        files_names = []
        for i in result['metadatas']:
            files_names.append(i['source'])
        return files_names

#%%
