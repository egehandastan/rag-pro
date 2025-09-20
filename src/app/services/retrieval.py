from pathlib import Path
from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from .embedding import get_embeddings

INDEX_DIR = Path("storage/faiss")
INDEX_NAME = "rag_index"

def _index_dir() -> Path:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    return INDEX_DIR

def save_store(store: FAISS):
    """Save FAISS store to local disk."""
    store.save_local(str(_index_dir()), index_name=INDEX_NAME)

def load_store() -> Optional[FAISS]:
    """Load FAISS store if it exists, otherwise return None."""
    faiss_file = _index_dir() / f"{INDEX_NAME}.faiss"
    pkl_file = _index_dir() / f"{INDEX_NAME}.pkl"
    if faiss_file.exists() and pkl_file.exists():
        return FAISS.load_local(
            str(_index_dir()),
            embeddings=get_embeddings(),
            index_name=INDEX_NAME,
            allow_dangerous_deserialization=True
        )
    return None

def create_or_load(initial_docs: Optional[List[Document]] = None) -> FAISS:
    """
    Create a new FAISS store (if none exists) or load existing one.
    If creating new, require initial_docs to bootstrap the index.
    """
    store = load_store()
    if store is None:
        if not initial_docs or len(initial_docs) == 0:
            raise ValueError("No existing FAISS index and no initial documents provided.")
        store = FAISS.from_documents(initial_docs, get_embeddings())
        save_store(store)
    return store

def add_documents(docs: List[Document]) -> int:
    """Add new documents to the FAISS store and persist them."""
    store = load_store()
    if store is None:
        # If no index exists, bootstrap with these docs
        store = create_or_load(docs)
    else:
        store.add_documents(docs)
        save_store(store)
    return len(docs)

def similarity_search(query: str, k: int = 3) -> List[Document]:
    """Search for top-k similar documents."""
    store = load_store()
    if store is None:
        return []
    return store.similarity_search(query, k=k)
