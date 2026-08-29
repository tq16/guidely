from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        description="The question asked by the user.",
    )


class TextDocumentUpdate(BaseModel):
    content: str = Field(
        ...,
        description="The updated content of an uploaded TXT document.",
    )