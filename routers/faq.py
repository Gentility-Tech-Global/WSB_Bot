from fastapi import APIRouter
from pydantic import BaseModel
import openai

router = APIRouter()

class Question(BaseModel):
    query: str

@router.post("/ask")
def ask_question(q: Question):
    # Requires `OPENAI_API_KEY` setup in your environment
    openai.api_key = "your-openai-key"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": q.query}]
    )
    return {"answer": response.choices[0].message["content"]}

