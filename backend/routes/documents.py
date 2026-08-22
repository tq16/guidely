from fastapi import APIRouter
from backend.services.document_service import load_sample_documents

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.get("/sample")
def get_sample_documents():
    documents = load_sample_documents()

    return {
        "document_count": len(documents),
        "documents": documents,
    }
    
    