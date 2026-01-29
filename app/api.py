from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from app.rag import answer_query

app = FastAPI()


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


@app.post("/query")
def query_emails(
    request: QueryRequest,
    x_user_id: str = Header(...)
):
    try:
        return answer_query(
            user_id=x_user_id,
            question=request.question,
            top_k=request.top_k
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
