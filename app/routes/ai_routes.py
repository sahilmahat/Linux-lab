from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")
router = APIRouter(prefix="/ai", tags=["ai"])

class AIQuery(BaseModel):
    question: str

@router.post("/ask")
def ask_ai(query: AIQuery):
    if not query.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        prompt = f"""You are LinuxLab AI, an expert Linux troubleshooting assistant.
A user has asked the following Linux question:

{query.question}

Provide a clear, step-by-step solution. Format your response like this:
- Use numbered steps
- Include actual Linux commands wrapped in backticks
- Keep it concise and practical
- Maximum 6 steps
- End with a tip if relevant"""

        response = model.generate_content(prompt)
        return {
            "question": query.question,
            "answer": response.text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")
