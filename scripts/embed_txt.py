# Run with: PYTHONPATH=. python scripts/embed_txt.py
from pathlib import Path
from src.app.services.loaders import load_txt
from src.app.services.chunk import simple_chunk_text
from src.app.services.embedding import get_embeddings

# Load the text file
text = load_txt(Path("data/raw/sample.txt"))

# Split into chunks
chunks = simple_chunk_text(text, chunk_size=50, chunk_overlap=10)

# Get the embedding model
emb = get_embeddings()

# Generate embeddings for the first 3 chunks
vectors = emb.embed_documents(chunks[:3])

print("Generated", len(vectors), "embeddings.")
print("Dimension of each vector:", len(vectors[0]))
print("Preview of first vector (first 10 dims):", vectors[0][:10])
