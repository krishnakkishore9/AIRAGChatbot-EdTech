from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import uuid

import traceback
import sys
import os

# Ensure the backend directory is in the path so rag_chatbot can be found
sys.path.insert(0, os.path.dirname(__file__))

try:
    from rag_chatbot import get_bot_response
    RAG_IMPORT_ERROR = None
except Exception as e:
    get_bot_response = None
    RAG_IMPORT_ERROR = traceback.format_exc()

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

@app.get("/api/health")
def health():
    import os
    return {
        "status": "ok",
        "rag_import_error": RAG_IMPORT_ERROR,
        "GEMINI_API_KEY_set": bool(os.getenv("GEMINI_API_KEY")),
        "OPENROUTER_API_KEY_set": bool(os.getenv("OPENROUTER_API_KEY")),
        "SUPABASE_URL_set": bool(os.getenv("SUPABASE_URL")),
        "PINECONE_KEY_set": bool(os.getenv("PINECONE_KEY")),
    }

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    """
    Standard JSON API endpoint for the React/Next.js frontend.
    """
    if RAG_IMPORT_ERROR:
        raise HTTPException(status_code=500, detail=f"RAG module failed to load: {RAG_IMPORT_ERROR}")
    try:
        reply = get_bot_response(req.message, req.user_id)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
