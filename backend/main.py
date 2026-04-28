from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import uuid

from rag_chatbot import get_bot_response

app = FastAPI(title="School RAG API")

# Setup CORS for the frontend to communicate with this backend API
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://airag-chatbot-ed-tech.vercel.app" # <-- Make sure to include https://!
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    user_id: str

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    """
    Standard JSON API endpoint for the React/Next.js frontend.
    """
    try:
        reply = get_bot_response(req.message, req.user_id)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
