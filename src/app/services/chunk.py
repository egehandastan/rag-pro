from typing import Optional

def simple_chunk_text(text: str, chunk_size: Optional[int] = 800, chunk_overlap: Optional[int] = 120):
    """
   Splits the text into chunks.
    - chunk_size: maximum length of each chunk
    - chunk_overlap: number of characters to overlap between chunks
    """
    cs = chunk_size or 800
    co = chunk_overlap or 120
    out = []
    i = 0
    n = len(text)
    while i < n:
        out.append(text[i:i+cs])
        i += max(1, cs - co)
    return [c for c in out if c.strip()]
