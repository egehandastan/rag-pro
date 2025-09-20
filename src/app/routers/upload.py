from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil

router = APIRouter(prefix="/api/v1/upload", tags=["upload"])

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    # Allow TXT and PDF
    ext = file.filename.split(".")[-1].lower()
    if ext not in ["txt", "pdf"]:
        raise HTTPException(status_code=400, detail="Only .txt and .pdf files are supported")

    # Save file to uploads folder
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "path": str(file_path)}
