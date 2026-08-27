from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel

from backend.services.document_service import load_sample_documents
from backend.services.upload_service import (
    delete_uploaded_document,
    get_uploaded_text_content,
    list_uploaded_documents,
    save_uploaded_document,
    update_uploaded_text_content,
)
from backend.services.vector_service import index_documents

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


class TextDocumentUpdate(BaseModel):
    content: str


@router.get("/sample")
def get_sample_documents():
    documents = load_sample_documents()

    return {
        "document_count": len(documents),
        "documents": documents,
    }


@router.get("/uploaded")
def get_uploaded_documents():
    documents = list_uploaded_documents()

    return {
        "document_count": len(documents),
        "documents": documents,
    }


@router.get("/uploaded/{file_name}/content")
def get_uploaded_document_content(file_name: str):
    return get_uploaded_text_content(file_name)


@router.put("/uploaded/{file_name}/content")
def update_uploaded_document_content(
    file_name: str,
    request: TextDocumentUpdate,
):
    update_result = update_uploaded_text_content(file_name, request.content)
    index_result = index_documents(force_reindex=True)

    return {
        **update_result,
        "index": index_result,
    }


@router.post("/upload")
def upload_document(file: UploadFile = File(...)):
    upload_result = save_uploaded_document(file)
    index_result = index_documents(force_reindex=True)

    return {
        **upload_result,
        "index": index_result,
    }


@router.delete("/uploaded/{file_name}")
def delete_document(file_name: str):
    delete_result = delete_uploaded_document(file_name)
    index_result = index_documents(force_reindex=True)

    return {
        **delete_result,
        "index": index_result,
    }


@router.post("/reindex")
def reindex_documents():
    return index_documents(force_reindex=True)


@router.get("/index-status")
def get_index_status():
    return index_documents(force_reindex=False) 