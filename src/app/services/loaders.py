from pathlib import Path

def load_txt(path: Path) -> str:
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text(encoding="utf-8", errors="ignore")
