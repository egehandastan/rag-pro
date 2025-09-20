# Run with: PYTHONPATH=. python scripts/chunk_txt.py
from pathlib import Path
from src.app.services.loaders import load_txt
from src.app.services.chunk import simple_chunk_text

# Read sample file
text = load_txt(Path("data/raw/sample.txt"))

# Use small chunk size for testing
chunks = simple_chunk_text(text, chunk_size=50, chunk_overlap=10)

print("Chunk count:", len(chunks))
for i, c in enumerate(chunks, 1):
    print(f"\n--- Chunk {i} ---\n{c}")
