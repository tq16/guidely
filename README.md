````md
# Guidely

Guidely is an internal knowledge assistant that lets users upload company documents, ask questions in plain language, and receive AI-generated answers with source citations.

## Features

- Ask questions in plain language
- Search documents by meaning using embeddings
- Generate answers with Gemini API
- Show source citations and similarity scores
- Upload TXT and PDF documents
- Automatically index uploaded documents
- View uploaded documents in a knowledge library
- Edit uploaded TXT documents
- Delete uploaded documents
- Reindex all documents manually

## Tech Stack

### Frontend

- React
- Vite
- CSS

### Backend

- FastAPI
- FAISS
- Sentence Transformers
- Gemini API
- PyPDF
- Python

## How It Works

1. A user uploads a TXT or PDF document.
2. Guidely reads the text and splits it into smaller chunks.
3. Sentence Transformers converts every chunk into an embedding.
4. FAISS stores the embeddings and searches for chunks with similar meaning.
5. The user asks a question.
6. Guidely finds the most relevant document chunks.
7. Gemini receives the question and relevant chunks.
8. Gemini generates a short answer using only the provided sources.
9. Guidely shows the answer, sources, snippets, and similarity scores.

## Project Structure

```text
guidely/
├── backend/
│   ├── routes/
│   │   ├── documents.py
│   │   └── search.py
│   ├── services/
│   │   ├── answer_service.py
│   │   ├── document_service.py
│   │   ├── upload_service.py
│   │   └── vector_service.py
│   └── main.py
├── data/
│   ├── sample-docs/
│   └── uploaded-docs/
├── frontend/
├── storage/
├── .env
├── requirements.txt
└── README.md
````

## Setup

### 1. Clone the Project

```bash
git clone <your-repository-url>
cd guidely
```

### 2. Set Up the Backend

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the main project folder:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Run the FastAPI backend:

```bash
uvicorn backend.main:app --reload --port 8000
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Set Up the Frontend

Open another terminal and run:

```bash
cd frontend
npm install
npm run dev
```

Open the URL shown in the terminal, usually:

```text
http://localhost:5173
```

## API Endpoints

| Method | Endpoint                                  | Description                                     |
| ------ | ----------------------------------------- | ----------------------------------------------- |
| POST   | `/search/ask`                             | Ask Guidely a question and receive an AI answer |
| GET    | `/search/`                                | Search relevant document chunks                 |
| POST   | `/documents/upload`                       | Upload and index a TXT or PDF document          |
| GET    | `/documents/uploaded`                     | List uploaded documents                         |
| GET    | `/documents/uploaded/{file_name}/content` | Read an uploaded TXT document                   |
| PUT    | `/documents/uploaded/{file_name}/content` | Edit and reindex an uploaded TXT document       |
| DELETE | `/documents/uploaded/{file_name}`         | Delete and reindex an uploaded document         |
| POST   | `/documents/reindex`                      | Rebuild the document search index               |
| GET    | `/documents/index-status`                 | Check the index status                          |

## Using Guidely

1. Open the frontend in your browser.
2. Upload a TXT or PDF document if needed.
3. Enter a question in the question box.
4. Click **Ask Guidely**.
5. Read the AI answer.
6. Check **Sources Used** to see the document chunks used for the answer.
7. Use the Knowledge Library to edit TXT files, delete files, or reindex all documents.

## Security

The Gemini API key is stored in the local `.env` file.

Do not upload `.env` to GitHub. Add this to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
storage/
data/uploaded-docs/
```

```
```
