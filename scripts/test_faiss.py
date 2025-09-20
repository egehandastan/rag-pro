# Run with: PYTHONPATH=. python scripts/test_faiss.py
from pathlib import Path
from langchain_core.documents import Document
from src.app.services.loaders import load_txt
from src.app.services.chunk import simple_chunk_text
from src.app.services.retrieval import add_documents, similarity_search

# Load text
text = load_txt(Path("data/raw/sample.txt"))

# Split into chunks
chunks = simple_chunk_text(text, chunk_size=50, chunk_overlap=10)

# Convert to Document objects
docs = [Document(page_content=c, metadata={"source": "sample.txt"}) for c in chunks]

# Add to FAISS
added = add_documents(docs)
print(f"Added {added} chunks to FAISS index.")

# Run a similarity search
query = "What does this project?"
results = similarity_search(query, k=2)

print("\nTop results:")
for i, doc in enumerate(results, 1):
    print(f"--- Result {i} ---")
    print("Source:", doc.metadata.get("source"))
    print("Content:", doc.page_content[:200])
