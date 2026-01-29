import json
import requests
from typing import List, Dict

from app.embedder import Embedder
from app.vector_store import FaissStore
from app.config import settings


MAX_CONTEXT_CHARS = 2000
LLM_TIMEOUT = 180


def call_llm(context: str, question: str) -> str:
    prompt = f"""You are a personal email assistant.

Use ONLY the email content below to answer the user's question.
If the answer is not present, say you do not have enough information.

Emails:
{context}

Question:
{question}

Answer in clear, natural language.
"""

    response = requests.post(
        settings.OLLAMA_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "top_p": 0.9
            }
        }),
        timeout=LLM_TIMEOUT
    )

    response.raise_for_status()

    answer = response.json().get("response", "").strip()
    if not answer:
        raise RuntimeError("Empty LLM response")

    return answer


def answer_query(user_id: str, question: str, top_k: int = 5) -> Dict:
    store = FaissStore(user_id)
    embedder = Embedder()

    query_vector = embedder.embed([question])[0]
    results = store.search(query_vector, top_k=top_k)

    if not results:
        return {
            "answer": "No relevant emails were found for your question.",
            "sources": []
        }

    context_blocks: List[str] = []
    sources: List[Dict] = []

    for r in results:
        context_blocks.append(
            f"Subject: {r['subject']}\n"
            f"From: {r['sender']}\n"
            f"Date: {r['timestamp']}\n"
            f"Content: {r['text']}\n"
        )
        sources.append({
            "subject": r["subject"],
            "sender": r["sender"],
            "timestamp": r["timestamp"]
        })

    context = "\n---\n".join(context_blocks)
    context = context[:MAX_CONTEXT_CHARS]

    try:
        answer = call_llm(context, question)
    except Exception as e:
        return {
            "answer": f" LLM failed to generate a response: {str(e)}",
            "sources": sources
        }

    return {
        "answer": answer,
        "sources": sources
    }
