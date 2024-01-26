from sqlmodel import Field, SQLModel


class PDFBase(SQLModel):
    name: str
    ids: str
    description: str
    vector_id: str
    system_prompt: str
    context_prompt: str
    show: bool = True


class PDFIndexer(PDFBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class PDFCreate(PDFBase):
    pass


class PDFRead(PDFBase):
    id: int
