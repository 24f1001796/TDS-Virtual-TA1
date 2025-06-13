from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import requests

app = FastAPI()

class Link(BaseModel):
    url: str
    text: str

class AnswerResponse(BaseModel):
    answer: str
    links: List[Link]

class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None

OLLAMA_URL = "http://localhost:11434/api/generate"

@app.post("/api/", response_model=AnswerResponse)
async def answer_question(req: QuestionRequest):
    prompt = f"Student asked: {req.question}\nProvide a concise answer and relevant links from TDS Discourse and course content."
    data = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=data)
    answer_text = response.json().get("response", "No answer generated.")
    # Dummy links for now; replace with real retrieval logic
    links = [
        {"url": "https://discourse.onlinedegree.iitm.ac.in/t/example", "text": "Sample discussion"}
    ]
    return {"answer": answer_text, "links": links}
