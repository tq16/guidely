import logging
import time

from fastapi import APIRouter, HTTPException, Query

from backend.models.schemas import QuestionRequest
from backend.services.answer_service import generate_answer
from backend.services.metrics_service import (
    record_failure,
    record_latency,
)
from backend.services.vector_service import search_chunks

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.get("/")
def search_documents(
    q: str = Query(..., description="Question to search for"),
    top_k: int = Query(3, ge=1, le=5),
):
    clean_query = q.strip()

    if not clean_query:
        record_failure("empty_query")

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        results = search_chunks(clean_query, top_k)

    except Exception:
        logger.exception("Document search failed")
        record_failure("search_error")

        raise HTTPException(
            status_code=500,
            detail="Document search is currently unavailable.",
        )

    if not results:
        record_failure("no_results")

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
        record_failure("empty_query")

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        sources = search_chunks(question, top_k=3)

    except Exception:
        logger.exception("Document search failed")
        record_failure("search_error")

        raise HTTPException(
            status_code=500,
            detail="Document search is currently unavailable.",
        )

    if not sources:
        record_failure("no_results")

        raise HTTPException(
            status_code=404,
            detail="No relevant document chunks were found.",
        )

    try:
        answer = generate_answer(question, sources)

    except ValueError as error:
        record_failure("missing_or_invalid_api_key")

        raise HTTPException(
            status_code=503,
            detail=str(error),
        )

    except Exception as error:
        logger.exception("Gemini answer generation failed")
        record_failure("gemini_api_error")

        raise HTTPException(
            status_code=502,
            detail=f"Gemini error: {error}",
        )

    latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

    record_latency(latency_ms)

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