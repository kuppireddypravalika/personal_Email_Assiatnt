import mailbox
from bs4 import BeautifulSoup
from typing import List, Dict

def extract_body(msg) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode("utf-8", errors="ignore")

        for part in msg.walk():
            if part.get_content_type() == "text/html":
                payload = part.get_payload(decode=True)
                if payload:
                    html = payload.decode("utf-8", errors="ignore")
                    return BeautifulSoup(html, "html.parser").get_text(" ", strip=True)

        return ""

    payload = msg.get_payload(decode=True)
    if payload:
        return payload.decode("utf-8", errors="ignore")
    return ""

def load_mbox(path: str) -> List[Dict]:
    mbox = mailbox.mbox(path)
    emails = []

    for msg in mbox:
        emails.append({
            "message_id": str(msg.get("Message-ID", "")),
            "sender": str(msg.get("From", "")),
            "subject": str(msg.get("Subject", "")),
            "timestamp": str(msg.get("Date", "")),
            "body": extract_body(msg)
        }) 

    return emails
