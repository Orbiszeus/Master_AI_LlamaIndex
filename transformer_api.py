from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import transformer
import llama_based_retrieval
import uuid
from repository import db_connector
from fastapi import Form


app = FastAPI()

transformer_model = transformer.Transformer()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class PDFResponse(BaseModel):
    texts: List[List[str]]

class ErrorResponse(BaseModel):
    error: str

class Question(BaseModel):
    question : str
    uniqueId : str
    
class Organization(BaseModel):
    organizationName : str
    
class Country(BaseModel):
    countryName : str
    
CUSTOM_QUERY = "Send me a summary of the file. In your summary, make sure not to mention the file location nor the data name, also to have 10 bullet points. Each bullet point should be on a new row. Try to incorporate few key points from all the text. Do it step by step:"
    
@app.post("/upload_pdf")
def upload_pdf(files: list[UploadFile] = [], file_extension_list: List[str] = Form(...)):
    unique_id = str(uuid.uuid4())
    
    if not files:
        return JSONResponse(content={"error": "No files provided"}, status_code=400)
    try:
        
        parsed_pdf_list = transformer_model.parse_files(files, unique_id, file_extension_list)
        
        llama_based_retrieval.create_index(parsed_pdf_list[2], unique_id)
        
        auto_summarization = llama_based_retrieval.auto_summarization(unique_id)
        parsed_pdf_list[0]["autoSummary"] = str(auto_summarization)
        
        return parsed_pdf_list[0]

    except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/question")
def ask_question_to_ebuddy(question: Question):
    try:
        return llama_based_retrieval.ask_question(question.question, question.uniqueId)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)    


@app.post("/organization")
def get_organization_details(organizationName : Organization):
    print(organizationName.organizationName)
    organizationID = db_connector.addOrganization(organizationName.organizationName)
    return organizationID

@app.post("/country")
def send_user_data():
    return ""