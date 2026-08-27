from pathlib import Path

from fastapi import HTTPException, UploadFile
from pypdf import PdfReader


PROJECT_ROOT = Path(__file__).resolve().parents[2]
UPLOADED_DOCS_PATH = PROJECT_ROOT / "data" / "uploaded-docs"

ALLOWED_EXTENSIONS = {".txt", ".pdf"}


def get_uploaded_file_path(file_name: str) -> Path:
    safe_file_name = Path(file_name).name

    if safe_file_name != file_name:
        raise HTTPException(
            status_code=400,
            detail="Invalid file name.",
        )

    file_path = UPLOADED_DOCS_PATH / safe_file_name

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Uploaded document was not found.",
        )

    return file_path


def save_uploaded_document(file: UploadFile) -> dict:
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please select a document.",
        )

    safe_file_name = Path(file.filename).name
    extension = Path(safe_file_name).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only .txt and .pdf files are allowed.",
        )

    UPLOADED_DOCS_PATH.mkdir(parents=True, exist_ok=True)

    destination = UPLOADED_DOCS_PATH / safe_file_name

    with destination.open("wb") as saved_file:
        saved_file.write(file.file.read())

    return {
        "message": "Document uploaded successfully.",
        "file_name": safe_file_name,
    }


def read_uploaded_file(file_path: Path) -> str:
    if file_path.suffix.lower() == ".txt":
        return file_path.read_text(encoding="utf-8").strip()

    if file_path.suffix.lower() == ".pdf":
        reader = PdfReader(str(file_path))

        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        ).strip()

    return ""


def list_uploaded_documents() -> list[dict]:
    UPLOADED_DOCS_PATH.mkdir(parents=True, exist_ok=True)

    documents = []

    for file_path in sorted(UPLOADED_DOCS_PATH.iterdir()):
        if file_path.is_file() and file_path.suffix.lower() in ALLOWED_EXTENSIONS:
            documents.append(
                {
                    "file_name": file_path.name,
                    "file_type": file_path.suffix.lower().replace(".", "").upper(),
                    "size_kb": round(file_path.stat().st_size / 1024, 1),
                }
            )

    return documents


def get_uploaded_text_content(file_name: str) -> dict:
    file_path = get_uploaded_file_path(file_name)

    if file_path.suffix.lower() != ".txt":
        raise HTTPException(
            status_code=400,
            detail="Only TXT documents can be edited in Guidely.",
        )

    return {
        "file_name": file_path.name,
        "content": file_path.read_text(encoding="utf-8"),
    }


def update_uploaded_text_content(file_name: str, content: str) -> dict:
    file_path = get_uploaded_file_path(file_name)

    if file_path.suffix.lower() != ".txt":
        raise HTTPException(
            status_code=400,
            detail="Only TXT documents can be edited in Guidely.",
        )

    if not content.strip():
        raise HTTPException(
            status_code=400,
            detail="Document content cannot be empty.",
        )

    file_path.write_text(content, encoding="utf-8")

    return {
        "message": "Document updated successfully.",
        "file_name": file_path.name,
    }


def delete_uploaded_document(file_name: str) -> dict:
    file_path = get_uploaded_file_path(file_name)

    file_path.unlink()

    return {
        "message": "Document deleted successfully.",
        "file_name": file_path.name,
    }