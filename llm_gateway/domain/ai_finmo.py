from typing import Protocol

from llm_gateway.domain.query import Query


class AIFinmoInterface(Protocol):
    def generate_query_response(self, query: Query):
        raise NotImplementedError("generate_query_response method not implemented")
