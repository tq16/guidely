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
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── routes/
│   │   ├── documents.py
│   │   ├── metrics.py
│   │   └── search.py
│   ├── services/
│   │   ├── answer_service.py
│   │   ├── document_service.py
│   │   ├── metrics_service.py
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
```

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
| GET    | `/metrics/`                               | View latency, cache, and failure metrics        |

## Using Guidely

1. Open the frontend in your browser.
2. Upload a TXT or PDF document if needed.
3. Enter a question in the question box.
4. Click **Ask Guidely**.
5. Read the AI answer.
6. Check **Sources Used** to see the document chunks used for the answer.
7. Use the Knowledge Library to edit TXT files, delete files, or reindex all documents.


## Testing and Metrics

Guidely was tested using five questions based on the five sample company documents. Each question was asked through the React frontend, which tested the complete flow from the user interface to FastAPI, FAISS retrieval, Gemini answer generation, and source display.

| Metric | Target | Test Result | Status |
|---|---:|---:|---|
| Retrieval@3 | At least 80% | 100% (5 out of 5 expected documents appeared in the top 3 sources) | Pass |
| Answer reference coverage | At least 90% | 100% (5 out of 5 answers included source citations) | Pass |
| Embedding cache effectiveness | 100% for unchanged documents | 100% (5 cache hits and 0 cache misses) | Pass |
| Median answer latency | Less than 3 seconds | 6.85 seconds | Not met |
| P95 answer latency | Less than 5 seconds | 24.02 seconds | Not met |
| Empty question handling | Clear 4xx response | HTTP 400 with “Question cannot be empty.” | Pass |
| No-result handling | Clear 4xx response | HTTP 404 with “No relevant document chunks were found.” | Pass |
| Invalid or corrupted document handling | Clear 4xx response | HTTP 422 with “The PDF file is corrupted or cannot be read.” | Pass |
| Gemini API failure handling | Clear 5xx response | HTTP 502 with a clear Gemini error message | Implemented |

The metrics are saved automatically in `storage/metrics.json` and can be viewed through the `GET /metrics/` endpoint.

The system records successful query latency, median latency, P95 latency, embedding cache hits and misses, and failure types. The retrieval and cache tests were repeated with unchanged documents. This produced five cache hits and no cache misses.

The current latency is affected mainly by the external Gemini API response time. The application still records and exposes actual response times instead of reporting artificial results.



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
