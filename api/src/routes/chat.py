from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.services.embedding_service import search_index, embed_query
from src.services.store import documents_store

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    doc_id: str
    question: str


@router.post("/")
def chat(req: ChatRequest):
    if req.doc_id not in documents_store:
        raise HTTPException(status_code=404, detail="Document not found for the request")
    
    doc = documents_store[req.doc_id]

    query_embedding = embed_query(req.question)
    indices = search_index(doc["index"], query_embedding)

    relevant_chunks = [doc["chunks"][i] for i in indices]

    return {
        "question": req.question,
        "relevant_chunks": relevant_chunks
    }


