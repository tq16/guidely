from pathlib import Path


# Finds: guidely/data/sample-docs/
SAMPLE_DOCS_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "sample-docs"
)


def chunk_text(text: str, chunk_size: int = 80, overlap: int = 15) -> list[str]:
    """
    Splits text into small overlapping word chunks.

    Overlap means a few words appear in both chunks,
    so important information is not cut in the middle.
    """
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        if end >= len(words):
            break

        start += chunk_size - overlap

    return chunks


def load_sample_documents() -> list[dict]:
    """
    Reads all .txt files in data/sample-docs
    and returns document information plus chunks.
    """
    documents = []

    for file_path in SAMPLE_DOCS_PATH.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8").strip()
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

