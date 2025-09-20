from fastapi import FastAPI
from .core.config import settings

app = FastAPI(
    title="RAG Pro API",
    version="0.1.0",
    description="Temel iskelet: FastAPI + /health",
)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "host": settings.APP_HOST,
        "port": settings.APP_PORT
    }
