import json

import numpy as np
from langchain.embeddings import HuggingFaceEmbeddings

from llm_gateway.embedding_creator.embedding_creator import TextEmbedder
from llm_gateway.embedding_creator.gte.gte_config import GTEConfig


class GTEEmbeddingCreator(TextEmbedder):
    def __init__(self):
        self.model = None

    def initialize_embedding_model(self):
        self.model = HuggingFaceEmbeddings(model_name=GTEConfig.base_model, cache_folder=GTEConfig.cache_folder)

    def create_embeddings(self, text: str):
        embeddings = np.array(self.model.embed_query(text))
        return json.dumps({"text": text, "embeddings": embeddings.tolist()})
