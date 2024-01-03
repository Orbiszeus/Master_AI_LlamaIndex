from typing import List

from langchain.prompts import FewShotPromptTemplate, PromptTemplate

from llm_gateway.application.prompts import SYSTEM, HISTORICAL_FILE, SUFFIX
from llm_gateway.domain.file_summary import FileSummary
from llm_gateway.domain.query import Query
from llm_gateway.response_generator.response_generator import Message, Role


class PromptCrafter:
    def format(self, query: Query, historical_files: List[FileSummary]):
        h_file_examples = list()

        if historical_files:
            for idx, h_file in enumerate(historical_files):
                h_file_examples.append(
                    {
                        "idx": idx,
                        "file_type": self.process_fstring(h_file.type.name),
                        "summary": self.process_fstring(h_file.summary)

                    }
                )
        new_query = self.process_fstring(query.query_text)
        human_prompt = FewShotPromptTemplate(
            examples=h_file_examples,
            example_prompt=PromptTemplate.from_template(HISTORICAL_FILE),
            example_separator="\n------\n",
            suffix=SUFFIX,
            input_variables=["new_query"]
        ).format(new_query=new_query)

        formatted_human_prompt = self.process_fstring(human_prompt)
        return self._format_messages(formatted_human_prompt)

    @staticmethod
    def _format_messages(human_prompt: str):
        messages_list = list()
        messages_list.append(Message(
            role=Role.SYSTEM,
            content=SYSTEM,
        ))
        messages_list.append(Message(role=Role.HUMAN,
                                     content=human_prompt))
        return messages_list

    @staticmethod
    def process_fstring(fstring: str):
        return fstring.replace("{", "{{").replace("}", "}}").replace("'", '"')
