from fastapi import APIRouter, HTTPException

from src.services.embedding_service import search_index, embed_query
from src.services.store import documents_store
from src.services.llm_service import generate_response
from src.models.models import ChatRequest

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
def chat(req: ChatRequest):
    if req.doc_id not in documents_store:
        raise HTTPException(status_code=404, detail="Document not found for the request")
    
    doc = documents_store[req.doc_id]

    query_embedding = embed_query(req.question)
    indices = search_index(doc["index"], query_embedding)

    relevant_chunks = [doc["chunks"][i] for i in indices]

    response = generate_response(req.question, relevant_chunks)

    return {
        "question": req.question,
        "relevant_chunks": relevant_chunks,
        "response": response
    }


