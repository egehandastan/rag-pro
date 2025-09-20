from pathlib import Path
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from langchain_core.documents import Document

from ..services.loaders import load_any
from ..services.chunk import simple_chunk_text   # ← dosya adı 'chunk.py' olmalı
from ..services.retrieval import add_documents

router = APIRouter(prefix="/api/v1/ingest", tags=["ingest"])

class IngestRequest(BaseModel):
    folder_path: str = Field(..., description="Folder containing TXT/PDF files")

class IngestResponse(BaseModel):
    processed_docs: int
    chunks_indexed: int

@router.post("/", response_model=IngestResponse)
def ingest_folder(req: IngestRequest):
    folder = Path(req.folder_path)
    if not folder.exists() or not folder.is_dir():
        raise HTTPException(status_code=400, detail=f"Folder not found: {folder}")

    files: List[Path] = [p for p in folder.glob("*") if p.suffix.lower() in {".txt", ".pdf"}]
    if not files:
        raise HTTPException(status_code=400, detail="No TXT/PDF files found in folder")

    total_chunks = 0
    processed = 0

    for f in files:
        try:
            text = load_any(f)
            chunks = simple_chunk_text(text)  # uses defaults (e.g., 800/120)
            docs = [Document(page_content=c, metadata={"source": f.name}) for c in chunks]
            total_chunks += add_documents(docs)
            processed += 1
        except Exception as e:
            # Skip bad files but continue
            print(f"[INGEST] Skipping {f}: {e}")

    return IngestResponse(processed_docs=processed, chunks_indexed=total_chunks)
