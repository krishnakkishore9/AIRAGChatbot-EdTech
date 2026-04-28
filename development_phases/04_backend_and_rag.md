# Phase 4: Backend API & RAG Implementation (FastAPI)

**Goal:** Build the core logic of the RAG chatbot and expose it via a REST API endpoint.

## Steps:
1. **API Setup**
   - Implement `backend/main.py` using FastAPI.
   - Define Pydantic models for the `/api/chat` request (`message`, `user_id`).
   - Integrate Gradio using `gr.mount_gradio_app()` on a route (e.g., `/chat-ui`).
2. **RAG Logic Implementation**
   - Create `backend/rag_chatbot.py`.
   - Implement document retrieval: embed the user's query and query Pinecone.
   - Implement database retrieval tools: define `get_db_data(table_name)` using the Supabase client.
3. **Memory Integration**
   - Implement functions to fetch the latest 5 messages for a `user_id` from Supabase's `chat_history`.
   - Implement a function to save the new user query and assistant reply to the `chat_history`.
4. **LLM Orchestration**
   - Formulate the system prompt with context (History, Docs, DB Data).
   - Integrate OpenRouter API (`openai/gpt-4o-mini`).
   - (Optional/Advanced) Implement formal Tool Calling to let the LLM dynamically invoke `get_db_data`.
