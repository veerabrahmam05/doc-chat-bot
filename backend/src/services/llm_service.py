import requests

from src.config.env import settings

OLLAMA_URL = settings.ollama_url

def generate_response(question: str, context_chunks: list[str]):
    context = "\n\n".join(context_chunks)

    prompt = f"""
    You are a helpful assistant.

    Answer the question using ONLY the context below.

    Context:
    {context}

    Question:
    {question}
"""
    
    response = requests.post(
        url=OLLAMA_URL,
        json={
            "model": "gpt-oss:120b-cloud",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()

    return result.get("response", "")