from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.documents import router as documents_router


app = FastAPI(
    title="Guidely API",
    description="Internal knowledge assistant backend",
    version="1.0.0",
)

# Allows the React frontend to call this API later.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router)
@app.get("/")
def home():
    return {
        "message": "Guidely backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "guidely-backend"
    }
    