# Run with: PYTHONPATH=. python scripts/preview_txt.py
from pathlib import Path
from src.app.services.loaders import load_txt

# Previous file that was created before
p = Path("data/raw/sample.txt")

# Read file
text = load_txt(p)

# Wirte console
print("Length of text:", len(text))
print("Preview of text:", text[:100]) 
