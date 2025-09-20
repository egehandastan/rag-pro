from fastapi import FastAPI
from .core.config import settings
from .routers import ingest   

app = FastAPI(
    title="RAG Pro API",
    version="0.1.0",
    description="RAG system with FastAPI",
)

# Health endpoint
@app.get("/health")
def health():
    return {
        "status": "ok",
        "host": settings.APP_HOST,
        "port": settings.APP_PORT
    }

# Routers
app.include_router(ingest.router)
