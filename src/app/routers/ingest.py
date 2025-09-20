from pathlib import Path
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from langchain_core.documents import Document
from ..services.loaders import load_txt
from ..services.chunk import simple_chunk_text
from ..services.retrieval import add_documents

router = APIRouter(prefix="/api/v1/ingest", tags=["ingest"])

class IngestRequest(BaseModel):
    folder_path: str = Field(..., description="Folder containing TXT files")

class IngestResponse(BaseModel):
    processed_docs: int
    chunks_indexed: int

@router.post("/", response_model=IngestResponse)
def ingest_files(req: IngestRequest):
    folder = Path(req.folder_path)

    if not folder.exists() or not folder.is_dir():
        raise HTTPException(status_code=400, detail=f"Folder not found: {folder}")

    txt_files = list(folder.glob("*.txt"))
    if not txt_files:
        raise HTTPException(status_code=400, detail="No TXT files found in folder")

    total_chunks = 0
    for f in txt_files:
        text = load_txt(f)
        chunks = simple_chunk_text(text)
        docs = [Document(page_content=c, metadata={"source": f.name}) for c in chunks]
        total_chunks += add_documents(docs)

    return IngestResponse(processed_docs=len(txt_files), chunks_indexed=total_chunks)
