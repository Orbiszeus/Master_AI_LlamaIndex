import asyncio
from fastapi import FastAPI, UploadFile, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
import transformer
import llama_based_retrieval
import uuid
from repository import db_connector
from fastapi import Form
from db.session import get_session
from db.models.pdf import PDFCreate, PDFIndexer


app = FastAPI()

transformer_model = transformer.Transformer()


origins = ["*", "http://222.252.28.9:8060"]
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
    question: str
    uniqueId: str


class Organization(BaseModel):
    organizationName: str


class Country(BaseModel):
    countryName: str


CUSTOM_QUERY = "Send me a summary of the file. In your summary, make sure not to mention the file location nor the data name, also to have 10 bullet points. Each bullet point should be on a new row. Try to incorporate few key points from all the text. Do it step by step:"


@app.post("/upload_pdf")
def upload_pdf(
    files: list[UploadFile] = [],
    file_extension_list: List[str] = Form(...),
    prompt: List[str] = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    session: Session = Depends(get_session),
):
    unique_id = str(uuid.uuid4())

    if not files:
        return JSONResponse(content={"error": "No files provided"}, status_code=400)
    try:
        parsed_pdf_list = transformer_model.parse_files(
            files, unique_id, file_extension_list
        )

        llama_based_retrieval.create_index(parsed_pdf_list[2], unique_id)

        auto_summarization = llama_based_retrieval.auto_summarization(unique_id)
        parsed_pdf_list[0]["autoSummary"] = str(auto_summarization)
        pdf = PDFIndexer(
            ids=str(unique_id),
            name=name,
            description=description,
            vector_id="storage_" + str(unique_id),
            system_prompt=" ".join(prompt),
            context_prompt="",
            show=True,
        )
        print(pdf)
        session.add(pdf)
        session.commit()
        session.refresh(pdf)

        return parsed_pdf_list[0]

    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/pdf/{id}")
def get_pdf(id: str, session: Session = Depends(get_session)):
    statement = select(PDFIndexer).where(PDFIndexer.ids == id)
    pdf = session.exec(statement).one_or_none()
    if not pdf:
        return JSONResponse(content={"error": "No pdf found"}, status_code=400)

    return pdf


@app.put("/pdf/{id}")
def update_pdf(id: str, pdf: PDFCreate, session: Session = Depends(get_session)):
    statement = select(PDFIndexer).where(PDFIndexer.ids == id)
    pdf_db = session.exec(statement).one_or_none()
    if not pdf_db:
        return JSONResponse(content={"error": "No pdf found"}, status_code=400)

    pdf_db.name = pdf.name
    pdf_db.description = pdf.description
    pdf_db.system_prompt = pdf.system_prompt
    pdf_db.context_prompt = pdf.context_prompt
    pdf_db.show = pdf.show

    session.add(pdf_db)
    session.commit()
    session.refresh(pdf_db)

    return pdf_db


@app.post("/questions")
def ask_question_to_ebuddy(question: Question, session: Session = Depends(get_session)):
    async def astreamer(generator):
        try:
            for i in generator:
                yield (i)
                await asyncio.sleep(0.1)
        except asyncio.CancelledError as e:
            print("cancelled")

    try:
        # answer = llama_based_retrieval.ask_question(
        #     question.question, question.uniqueId
        # )

        # print(answer)

        # return JSONResponse(content=answer, status_code=200)
        statement = select(PDFIndexer).where(PDFIndexer.ids == question.uniqueId)
        pdf = session.exec(statement)
        system_prompt = pdf.one_or_none().system_prompt
        return StreamingResponse(
            astreamer(
                llama_based_retrieval.ask_questions(
                    question.question, question.uniqueId, system_prompt
                ).response_gen
            ),
            media_type="text/event-stream",
        )

    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/pdfs", response_model=List[PDFIndexer])
def get_pdfs(session: Session = Depends(get_session)):
    statement = select(PDFIndexer)  # .where(PDFIndexer.show)
    pdfs = session.exec(statement).all()
    if not pdfs:
        return JSONResponse(content={"error": "No pdfs found"}, status_code=400)

    return pdfs


@app.post("/question")
def ask_question_to_ebuddy(question: Question):
    async def astreamer(generator):
        try:
            for i in generator:
                yield (i)
                await asyncio.sleep(0.1)
        except asyncio.CancelledError as e:
            print("cancelled")

    try:
        # answer = llama_based_retrieval.ask_question(
        #     question.question, question.uniqueId
        # )

        # print(answer)

        # return JSONResponse(content=answer, status_code=200)
        return StreamingResponse(
            astreamer(
                llama_based_retrieval.ask_question(
                    question.question, question.uniqueId
                ).response_gen
            ),
            media_type="text/event-stream",
        )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/test-question")
def ask_question_to_ebuddy(question: Question):
    async def astreamer(generator):
        try:
            for i in generator:
                yield (i)
                await asyncio.sleep(0.1)
        except asyncio.CancelledError as e:
            print("cancelled")

    try:
        return StreamingResponse(
            astreamer(
                llama_based_retrieval.test_question(
                    question.question, question.uniqueId
                ).response_gen
            ),
            media_type="text/event-stream",
        )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/organization")
def get_organization_details(organizationName: Organization):
    print(organizationName.organizationName)
    organizationID = db_connector.addOrganization(organizationName.organizationName)
    return organizationID


@app.post("/country")
def send_user_data():
    return ""
