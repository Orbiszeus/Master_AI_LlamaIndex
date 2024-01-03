from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from llm_gateway.ai_finmo import AIFinmoLLM
from llm_gateway.domain.query import Query

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class ErrorResponse(BaseModel):
    error: str


@app.post("/generate_response")
def generate_response(user_query: Query):
    ai_finmo_resolution = AIFinmoLLM()
    return ai_finmo_resolution.generate_query_response(user_query)


@app.post("/create_embeddings")
def create_embeddings(text: str):
    ai_finmo_embeddings = AIFinmoLLM()
    return ai_finmo_embeddings.create_embeddings(text)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )
