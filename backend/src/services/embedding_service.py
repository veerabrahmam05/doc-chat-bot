from sentence_transformers import SentenceTransformer
from src.config.env import settings

HF_TOKEN = settings.hf_token

model = SentenceTransformer(model_name_or_path="all-MiniLM-L6-v2", token=HF_TOKEN)

def chunk_text(text: str, chunk_size = 500, overlap = 50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start = end - overlap
    
    return chunks

def generate_embeddings(chunks):
    return model.encode(chunks)
    
def search_index(index, query_embedding, top_K = 3):
    distances, indices = index.search(query_embedding, top_K)

    return indices[0]

def embed_query(query):
    return model.encode([query])

import faiss
import numpy as np

def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    return index