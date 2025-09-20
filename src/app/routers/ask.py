from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from openai import OpenAI
from ..services.retrieval import similarity_search
from ..core.config import settings

router = APIRouter(prefix="/api/v1/ask", tags=["ask"])

class AskRequest(BaseModel):
    query: str = Field(..., description="User question")
    top_k: Optional[int] = Field(default=3, description="Number of top results to retrieve")

class AskResponse(BaseModel):
    answer: str
    sources: List[str]

@router.post("/", response_model=AskResponse)
def ask_question(req: AskRequest):
    # Retrieve relevant chunks
    docs = similarity_search(req.query, k=req.top_k)
    if not docs:
        raise HTTPException(status_code=404, detail="No documents found in index")

    # Build context from chunks
    context = "\n\n".join([d.page_content for d in docs])

    # Query OpenAI with context + question
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    prompt = f"""
    You are an assistant that answers questions based on provided context.
    Context:
    {context}

    Question: {req.query}
    Answer in a clear and concise way.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    answer = response.choices[0].message.content

    return AskResponse(
        answer=answer,
        sources=[d.metadata.get("source", "unknown") for d in docs]
    )
