import enum
from dataclasses import dataclass
from typing import List, Any, Protocol

from langchain.prompts import ChatPromptTemplate


class Role(enum.Enum):
    HUMAN = 0
    SYSTEM = 1
    ASSISTANT = 2
    FUNCTION = 3


@dataclass
class Message:
    role: Role
    content: str


class ResponseGenerator(Protocol):
    chat_model: Any = None

    def construct_prompt(self, prompt_messages: List[Message]):
        messages_list = []

        for message in prompt_messages:
            if message.role == Role.SYSTEM:
                messages_list.append(("system", message.content))
            elif message.role == Role.HUMAN:
                messages_list.append(("human", message.content))
            elif message.role == Role.ASSISTANT:
                messages_list.append(("assistant", message.content))
            else:
                continue
        chat_template = ChatPromptTemplate.from_messages(messages_list)
        return chat_template.format()

    def construct_messages(self, prompt_messages: List[Message]):
        messages_list = []

        for message in prompt_messages:
            if message.role == Role.SYSTEM:
                messages_list.append({"role": "system", "content": message.content})
            elif message.role == Role.HUMAN:
                messages_list.append({"role": "user", "content": message.content})
            elif message.role == Role.ASSISTANT:
                messages_list.append({"role": "assistant", "content": message.content})
            else:
                continue
        return messages_list

    def generate_response(self, request: List[Message]):
        raise NotImplementedError("generate_response method not implemented")
