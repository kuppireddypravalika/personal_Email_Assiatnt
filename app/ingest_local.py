import argparse
from app.email_loader import load_mbox
from app.embedder import Embedder
from app.chunking import chunk_text
from app.vector_store import FaissStore


def ingest_local(user_id: str, mbox_path: str):
    emails = load_mbox(mbox_path)
    embedder = Embedder()
    store = FaissStore(user_id)

    print(f"Loaded {len(emails)} emails from {mbox_path}")

    new_count = 0

    for e in emails:
        if e["message_id"] in store.existing_ids:
            continue  

        full_text = f"""
Subject: {e['subject']}
From: {e['sender']}
Date: {e['timestamp']}

{e['body']}
"""

        chunks = chunk_text(full_text)
        if not chunks:
            continue

        vectors = embedder.embed(chunks)

        metas = [{
            "message_id": e["message_id"],
            "subject": e["subject"],
            "sender": e["sender"],
            "timestamp": e["timestamp"],
            "text": ch
        } for ch in chunks]

        store.add(vectors, metas)
        new_count += 1

    print(f" Ingestion complete ({new_count} new emails added)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user_id", required=True)
    parser.add_argument("--mbox", required=True)
    args = parser.parse_args()

    ingest_local(args.user_id, args.mbox)
