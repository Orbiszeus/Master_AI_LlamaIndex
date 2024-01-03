import re

from llm_gateway.domain.query_response import QueryResolution

pattern_response = re.compile(".*?<Response>(.*?)</Response>", flags=re.DOTALL + re.IGNORECASE)


def postprocess_response(id: int, llm_response: str):
    found_response = pattern_response.search(llm_response)
    responses = found_response.group(1)

    return QueryResolution(
        id=id,
        response=responses
    )
