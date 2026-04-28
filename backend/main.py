from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import gradio as gr
import uvicorn
import uuid

from rag_chatbot import get_bot_response

app = FastAPI(title="School RAG API")

# Setup CORS for the frontend to communicate with this backend API
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "airag-chatbot-ed-tech.vercel.app" # <-- Add your Vercel URL here!
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

# ==========================================
# Gradio ChatInterface Integration
# ==========================================

# A standalone Gradio chat function that auto-generates a UUID for testing purposes
def gradio_chat(message, history):
    # In a real UI with auth, the user_id comes from the JWT.
    # For Gradio testing, we'll use a valid standard UUID
    test_user_id = "00000000-0000-0000-0000-000000000000"
    return get_bot_response(message, test_user_id)

# Create the Gradio interface
demo = gr.ChatInterface(
    fn=gradio_chat,
    title="🎓 School Virtual Assistant",
    description="Ask me anything about fees, holidays, textbooks, or school policies!"
)

# Mount the Gradio app onto FastAPI at the /chat-ui route
app = gr.mount_gradio_app(app, demo, path="/chat-ui")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
