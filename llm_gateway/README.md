Create a new virtual_env and activate

```commandline
python3 -m venv <env_name>
source <env_name>/bin.activate
```

Install the dependencies

```commandline
make setup
```

To run the service

1. In the `llm_gateway/response_generator/openai/openai_config.py`, add your `OPENAI` Key
2. Use the below command

```commandline
make run_response_api
```

To test the functionality

1. Navigate to http://127.0.0.1:8000/docs
2. Click on the `Try it out` under `/generate_response` endpoint
3. Send a query with the `query_text` field

Note: Currently, in the demo version, we are only using two dummy summary files.

To Do [`/generate_response`]

- [ ] Add `embedding_generator` endpoint.
- [ ] Add the vector search capability and pick top 3-5.
- [ ] Pick the summaries of the top 3-5 files from the SQL tables.
- [ ] Transform the query result to `FileSummary` and retrieve the LLM response.

