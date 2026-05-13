from datetime import datetime
from bson import ObjectId
from src.models.schemas import Conversation
from fastapi import APIRouter, HTTPException, Depends

from src.services.store import documents_store
from src.services.llm_service import generate_response
from src.services.embedding_service import embed_query, search_index
from src.models.models import ChatRequest, User
from src.services.auth_service import get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def chat(req: ChatRequest, user: User = Depends(get_current_user)):
    # Validate document existence
    if req.doc_id not in documents_store:
        raise HTTPException(status_code=404, detail="Document not found for the request")

    doc = documents_store[req.doc_id]

    # Retrieve or create conversation
    if req.conversation_id:
        try:
            conv = await Conversation.get(ObjectId(req.conversation_id))
        except Exception:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conv = Conversation(user_id=user.id, doc_id=req.doc_id)
        await conv.insert()

    # Perform embedding and search
    query_embedding = embed_query(req.question)
    indices = search_index(doc["index"], query_embedding)
    relevant_chunks = [doc["chunks"][i] for i in indices]
    response = generate_response(req.question, relevant_chunks)

    # Save message to conversation
    message_entry = {
        "question": req.question,
        "response": response,
        "timestamp": datetime.utcnow().isoformat()
    }
    conv.messages.append(message_entry)
    await conv.save()

    return {
        "conversation_id": str(conv.id),
        "question": req.question,
        "relevant_chunks": relevant_chunks,
        "response": response
    }



