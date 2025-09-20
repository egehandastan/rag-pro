from langchain_openai import OpenAIEmbeddings
from ..core.config import settings

_embeddings = None

def get_embeddings():
    """
    Return a singleton instance of OpenAIEmbeddings.
    Loads the model defined in settings only once.
    """
    global _embeddings
    if _embeddings is None:
        _embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL_NAME,
            api_key=settings.OPENAI_API_KEY  
        )
    return _embeddings
