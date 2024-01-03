from dataclasses import dataclass
from os import environ


@dataclass
class OpenAIConfig:
    openai_api_key: str = environ.get("OPENAI_API_KEY", "<INSERT-OPENAI-KEY-HERE>")
    model_type: str = "CHAT"
