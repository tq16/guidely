from pathlib import Path

from backend.services.upload_service import (
    ALLOWED_EXTENSIONS,
    UPLOADED_DOCS_PATH,
    read_uploaded_file,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DOCS_PATH = PROJECT_ROOT / "data" / "sample-docs"


def chunk_text(text: str, chunk_size: int = 80, overlap: int = 15) -> list[str]:
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))

        if end >= len(words):
            break

        start += chunk_size - overlap

    return chunks


def load_sample_documents() -> list[dict]:
    """
    Reads both sample documents and uploaded documents.
    """
    documents = []

    file_paths = list(SAMPLE_DOCS_PATH.glob("*.txt"))

    if UPLOADED_DOCS_PATH.exists():
        for file_path in UPLOADED_DOCS_PATH.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in ALLOWED_EXTENSIONS:
                file_paths.append(file_path)

    for file_path in sorted(file_paths):
        if file_path.suffix.lower() == ".txt":
            text = file_path.read_text(encoding="utf-8").strip()
        else:
            text = read_uploaded_file(file_path)

        if not text:
            continue

        chunks = chunk_text(text)

        documents.append(
            {
                "file_name": file_path.name,
                "text": text,
                "chunks": chunks,
                "chunk_count": len(chunks),
            }
        )

    return documents