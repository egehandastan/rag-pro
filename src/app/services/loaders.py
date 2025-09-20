from pathlib import Path
import fitz  # PyMuPDF

def load_txt(path: Path) -> str:
    """Read a UTF-8 text file and return its content as a string."""
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text(encoding="utf-8", errors="ignore")

def load_pdf(path: Path) -> str:
    """Extract text from a PDF using PyMuPDF (fitz)."""
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    doc = fitz.open(path)
    pages = [p.get_text() for p in doc]
    return "\n".join(pages)

def load_any(path: Path) -> str:
    """Load .txt or .pdf and return plain text."""
    suf = path.suffix.lower()
    if suf == ".txt":
        return load_txt(path)
    if suf == ".pdf":
        return load_pdf(path)
    raise ValueError(f"Unsupported file type: {suf}")
