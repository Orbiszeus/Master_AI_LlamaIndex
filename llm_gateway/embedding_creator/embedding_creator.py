from typing import Protocol


class TextEmbedder(Protocol):
    def initialize_embedding_model(self):
        raise NotImplementedError("initialize_embedding_model method is not implemented")

    def create_embeddings(self, text: str):
        raise NotImplementedError("create_embeddings method is not implemented")
