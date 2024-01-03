from llm_gateway.application.post_processor import postprocess_response
from llm_gateway.application.prompt_crafter import PromptCrafter
from llm_gateway.domain.ai_finmo import AIFinmoInterface
from llm_gateway.domain.file_summary import FileType, FileSummary
from llm_gateway.domain.query import Query
from llm_gateway.gateway import Gateway


def _generate_hfiles_summaries():
    return [FileSummary(id=2, type=FileType.INFO, summary="GDP of China is 4 trillion"),
            FileSummary(id=2, type=FileType.FINANCE, summary="GDP of UK is 1 Trillion")]


class AIFinmoLLM(AIFinmoInterface):
    def __init__(self):
        self._prompt_crafter = PromptCrafter()

    def generate_query_response(self, query: Query):
        gateway = Gateway(response_model="OpenAI")

        formatted_prompt = self._prompt_crafter.format(query=query, historical_files=_generate_hfiles_summaries())
        response = gateway.generate_llm_response(messages=formatted_prompt)
        print([response["message"] for response in response["choices"]])
        try:
            processed_response = postprocess_response(id=query.id,
                                                      llm_response="\t".join(
                                                          response["message"]["content"] for response in
                                                          response["choices"]))
            print(processed_response)
        except:
            raise ValueError("No Response Generated!")

        return processed_response

    def create_embeddings(self, text: str):
        gateway = Gateway(embedding_model="gte")
        return gateway.create_embeddings(text)
