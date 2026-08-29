from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.documents import router as documents_router
from backend.routes.metrics import router as metrics_router
from backend.routes.search import router as search_router

app = FastAPI(
    title="Guidely API",
    description="Internal knowledge assistant backend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router)
app.include_router(search_router)
app.include_router(metrics_router)


@app.get("/")
def home():
    return {
        "message": "Guidely backend is running",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "guidely-backend",
    }