from llm_gateway.embedding_creator.gte.gte_embedding_creator import GTEEmbeddingCreator
from llm_gateway.response_generator.openai.openai_response_generator import OpenAIResponseGenerator


class Gateway:
    def __init__(self, embedding_model: str, response_model: str = None):
        if response_model:
            self.llm_response_model = OpenAIResponseGenerator()
        if embedding_model:
            self.llm_embedding_model = GTEEmbeddingCreator()
            self._initialize_models()

    def _initialize_models(self):
        if self.llm_embedding_model:
            self.llm_embedding_model.initialize_embedding_model()

    def generate_llm_response(self, messages):
        return self.llm_response_model.generate_response(messages)

    def create_embeddings(self, text: str):
        return self.llm_embedding_model.create_embeddings(text)
