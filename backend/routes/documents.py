import logging

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.models.schemas import TextDocumentUpdate
from backend.services.document_service import load_sample_documents
from backend.services.metrics_service import record_failure
from backend.services.upload_service import (
    delete_uploaded_document,
    get_uploaded_text_content,
    list_uploaded_documents,
    save_uploaded_document,
    update_uploaded_text_content,
)
from backend.services.vector_service import index_documents

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


def reindex_documents_safely() -> dict:
    try:
        return index_documents(force_reindex=True)

    except ValueError as error:
        record_failure("document_index_error")

        raise HTTPException(
            status_code=422,
            detail=str(error),
        )

    except Exception:
        logger.exception("Document indexing failed")
        record_failure("document_index_error")

        raise HTTPException(
            status_code=500,
            detail="Documents could not be indexed.",
        )


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
    try:
        return get_uploaded_text_content(file_name)

    except HTTPException as error:
        record_failure("document_read_error")
        raise error


@router.put("/uploaded/{file_name}/content")
def update_uploaded_document_content(
    file_name: str,
    request: TextDocumentUpdate,
):
    try:
        update_result = update_uploaded_text_content(
            file_name,
            request.content,
        )

    except HTTPException as error:
        record_failure("document_update_error")
        raise error

    index_result = reindex_documents_safely()

    return {
        **update_result,
        "index": index_result,
    }


@router.post("/upload")
def upload_document(file: UploadFile = File(...)):
    try:
        upload_result = save_uploaded_document(file)

    except HTTPException as error:
        record_failure("invalid_or_corrupted_document")
        raise error

    index_result = reindex_documents_safely()

    return {
        **upload_result,
        "index": index_result,
    }


@router.delete("/uploaded/{file_name}")
def delete_document(file_name: str):
    try:
        delete_result = delete_uploaded_document(file_name)

    except HTTPException as error:
        record_failure("document_delete_error")
        raise error

    index_result = reindex_documents_safely()

    return {
        **delete_result,
        "index": index_result,
    }


@router.post("/reindex")
def reindex_documents():
    return reindex_documents_safely()


@router.get("/index-status")
def get_index_status():
    try:
        return index_documents(force_reindex=False)

    except Exception:
        logger.exception("Index status check failed")
        record_failure("index_status_error")

        raise HTTPException(
            status_code=500,
            detail="Index status is currently unavailable.",
        )