from dataclasses import dataclass

@dataclass
class Query:
    id: int
    query_text: str
