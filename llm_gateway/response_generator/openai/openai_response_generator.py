from typing import Any

import openai

from llm_gateway.response_generator.openai.openai_config import OpenAIConfig
from llm_gateway.response_generator.response_generator import ResponseGenerator


class OpenAIResponseGenerator(ResponseGenerator):
    def generate_response(self,
                          prompt: Any
                          ):
        openai.api_key = OpenAIConfig.openai_api_key

        # chat model
        if OpenAIConfig.model_type == "CHAT":
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.construct_messages(prompt)
            )

        # instruct model
        if OpenAIConfig.model_type == "INSTRUCT":
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=self.construct_prompt(prompt)
            )

        return response

