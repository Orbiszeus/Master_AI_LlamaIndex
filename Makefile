setup:
	pip install -r requirements.txt

run_llm_api:
	uvicorn llm_gateway.llm_api:app --reload

run_transformer_api:
	unicorn transformer_api:app --reload