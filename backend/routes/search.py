import logging
import time

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from backend.services.answer_service import generate_answer
from backend.services.vector_service import search_chunks

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


class QuestionRequest(BaseModel):
    question: str


@router.get("/")
def search_documents(
    q: str = Query(..., description="Question to search for"),
    top_k: int = Query(3, ge=1, le=5),
):
    clean_query = q.strip()

    if not clean_query:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    results = search_chunks(clean_query, top_k)

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No relevant document chunks were found.",
        )

    return {
        "query": clean_query,
        "result_count": len(results),
        "sources": results,
    }


@router.post("/ask")
def ask_question(request: QuestionRequest):
    start_time = time.perf_counter()
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    sources = search_chunks(question, top_k=3)

    if not sources:
        raise HTTPException(
            status_code=404,
            detail="No relevant document chunks were found.",
        )

    try:
        answer = generate_answer(question, sources)

    except ValueError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )

    except Exception as error:
        logger.exception("Gemini answer generation failed")

        raise HTTPException(
            status_code=502,
            detail=f"Gemini error: {error}",
        )

    latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

    logger.info(
        "Question answered | latency_ms=%s | source_count=%s",
        latency_ms,
        len(sources),
    )

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "latency_ms": latency_ms,
    }