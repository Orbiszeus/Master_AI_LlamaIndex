import os
import openai
import logging
import sys
import llama_index
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    load_index_from_storage,
    StorageContext,
    LLMPredictor,
    PromptHelper,
    ServiceContext,
)
from llama_index.llms import OpenAI
import chromadb
from llama_index.vector_stores import ChromaVectorStore
from llama_index.embeddings import OpenAIEmbedding
from trulens_eval import Tru
from llama_index.query_engine import CitationQueryEngine
import json

openai.api_key = os.environ["OPENAI_API_KEY"]


CUSTOM_QUERY = "First greet yourself and Send me a summary of the file. In your summary, make sure  to mention the file location and the data name, also to have 10 bullet points. Each bullet point should be on a new row. Try to incorporate few key points from all the text. Do it step by step:"
list_of_indices = []
tru = Tru()
tru.reset_database()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


def create_index(directory, unique_folder_id):
    llm = OpenAI(temperature=0.1, model="gpt-4-vision-preview", max_tokens=512)
    prompt_helper = PromptHelper(
        context_window=4096,
        num_output=256,
        chunk_overlap_ratio=0.1,
        chunk_size_limit=None,
    )

    service_context = ServiceContext.from_defaults(llm=llm, prompt_helper=prompt_helper)

    documents = SimpleDirectoryReader(input_dir=directory).load_data()

    index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    index.set_index_id(create_dynamic_vector_ids(unique_folder_id))
    index.storage_context.persist(create_dynamic_storage_contexts(unique_folder_id))
    a = index.index_struct_cls
    # Chroma vector store for easy indexing and retrieval

    db = chromadb.PersistentClient(path="./chroma_db")

    chroma_collection = db.get_or_create_collection("investment_ai")
    chroma_vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    chroma_storage_context = StorageContext.from_defaults(
        vector_store=chroma_vector_store
    )

    chroma_index = VectorStoreIndex.from_documents(
        documents,
        storage_context=chroma_storage_context,
        service_context=service_context,
    )
    print(chroma_index.storage_context.graph_store.get)
    return index


def auto_summarization(unique_folder_id):
    dynamic_storage_context = create_dynamic_storage_contexts(unique_folder_id)
    dynamic_vector_id = create_dynamic_vector_ids(unique_folder_id)
    storage_context = StorageContext.from_defaults(persist_dir=dynamic_storage_context)
    # load index
    index = load_index_from_storage(storage_context, index_id=dynamic_vector_id)
    query_engine = index.as_query_engine(response_mode="compact", verbose=True)
    response = query_engine.query(CUSTOM_QUERY)
    return str(response.response)

    return str(response.response)


def ask_question(query, unique_folder_id):
    dynamic_storage_context = create_dynamic_storage_contexts(unique_folder_id)
    dynamic_vector_id = create_dynamic_vector_ids(unique_folder_id)
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=dynamic_storage_context)
    # load index
    index = llama_index.indices.loading.load_index_from_storage(
        storage_context, index_id=dynamic_vector_id
    )
    query_engine = CitationQueryEngine.from_args(
        index, similarity_top_k=3, citation_chunk_size=512, streaming=True
    )
    response_stream = query_engine.query(
        "When a question is asked always and if it is a greeting please answer accordingly.If question is not about given data, say you only answer about given data. If the question is about the given data please eloborate more on details and answer human-like according to this question: "
        + query
    )
    return response_stream


def create_dynamic_storage_contexts(unique_folder_id):
    return "./storage_" + str(unique_folder_id)


def create_dynamic_vector_ids(unique_folder_id):
    return "vector_index_" + str(unique_folder_id)
