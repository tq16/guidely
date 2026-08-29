import hashlib
import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from backend.services.document_service import load_sample_documents
from backend.services.metrics_service import record_cache_event


PROJECT_ROOT = Path(__file__).resolve().parents[2]
STORAGE_PATH = PROJECT_ROOT / "storage"
INDEX_PATH = STORAGE_PATH / "guidely.index"
METADATA_PATH = STORAGE_PATH / "metadata.json"
STATE_PATH = STORAGE_PATH / "index_state.json"

MODEL_NAME = "all-MiniLM-L6-v2"
MIN_SIMILARITY_SCORE = 0.10

embedding_model = None


def get_embedding_model():
    global embedding_model

    if embedding_model is None:
        embedding_model = SentenceTransformer(MODEL_NAME)

    return embedding_model


def create_documents_signature(documents: list[dict]) -> str:
    content = ""

    for document in documents:
        content += document["file_name"] + document["text"]

    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def index_documents(force_reindex: bool = False) -> dict:
    """
    Creates embeddings and saves the FAISS index.
    Reuses the saved index when documents have not changed.
    """
    STORAGE_PATH.mkdir(exist_ok=True)

    documents = load_sample_documents()

    if not documents:
        raise ValueError("No documents are available for indexing.")

    signature = create_documents_signature(documents)

    if (
        not force_reindex
        and INDEX_PATH.exists()
        and METADATA_PATH.exists()
        and STATE_PATH.exists()
    ):
        saved_state = json.loads(STATE_PATH.read_text(encoding="utf-8"))

        if saved_state["documents_signature"] == signature:
            saved_metadata = json.loads(
                METADATA_PATH.read_text(encoding="utf-8")
            )

            record_cache_event(cache_hit=True)

            return {
                "message": "Index already exists. Used cached embeddings.",
                "cache_hit": True,
                "document_count": len(documents),
                "chunk_count": len(saved_metadata),
            }

    chunks = []

    for document in documents:
        for chunk_number, chunk_text in enumerate(document["chunks"]):
            chunks.append(
                {
                    "id": f"{document['file_name']}-chunk-{chunk_number}",
                    "file_name": document["file_name"],
                    "chunk_number": chunk_number,
                    "text": chunk_text,
                }
            )

    model = get_embedding_model()

    vectors = model.encode(
        [chunk["text"] for chunk in chunks],
        normalize_embeddings=True,
    )

    vectors = np.array(vectors, dtype="float32")

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    faiss.write_index(index, str(INDEX_PATH))

    METADATA_PATH.write_text(
        json.dumps(chunks, indent=2),
        encoding="utf-8",
    )

    STATE_PATH.write_text(
        json.dumps(
            {
                "documents_signature": signature,
                "model": MODEL_NAME,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # A forced reindex is intentional, so it does not count as a cache miss.
    if not force_reindex:
        record_cache_event(cache_hit=False)

    return {
        "message": "Documents indexed successfully.",
        "cache_hit": False,
        "document_count": len(documents),
        "chunk_count": len(chunks),
    }


def search_chunks(query: str, top_k: int = 3) -> list[dict]:
    """
    Converts a question into an embedding and returns
    the most similar stored document chunks.
    """
    index_documents(force_reindex=False)

    index = faiss.read_index(str(INDEX_PATH))

    metadata = json.loads(
        METADATA_PATH.read_text(encoding="utf-8")
    )

    model = get_embedding_model()

    query_vector = model.encode(
        [query],
        normalize_embeddings=True,
    )

    query_vector = np.array(query_vector, dtype="float32")

    scores, positions = index.search(query_vector, top_k)

    results = []

    for score, position in zip(scores[0], positions[0]):
        if position == -1 or float(score) < MIN_SIMILARITY_SCORE:
            continue

        chunk = metadata[position]

        results.append(
            {
                "file_name": chunk["file_name"],
                "chunk_number": chunk["chunk_number"],
                "snippet": chunk["text"],
                "similarity_score": round(float(score), 4),
            }
        )

    return results