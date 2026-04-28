from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4

from src.services.file_service import save_file, detect_file_type, extract_text_from_pdf
from src.services.embedding_service import chunk_text, generate_embeddings, create_faiss_index
from src.services.store import documents_store

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    file_path, file_ext = save_file(file)

    file_type = detect_file_type(file_ext)
    extracted_text = ""

    if file_type == "unsupported":
        raise HTTPException(status_code=400, detail="Unsupported file type")
    elif file_type == "pdf":
        extracted_text = extract_text_from_pdf(file_path)
        chunks = chunk_text(extracted_text)
        embeddings = generate_embeddings(chunks)
        index = create_faiss_index(embeddings)

        doc_id = str(uuid4())
        documents_store[doc_id] = {
            "chunks": chunks,
            "index": index
        }

    return {
        "doc_id": doc_id,
        "file_name": file.filename,
        "chunks len": len(chunks)
     }