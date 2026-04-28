# 📐 System Design Document: AI-Powered School Website + RAG Chatbot

## 1. High-Level Architecture

The system follows a modern decoupled architecture consisting of a frontend web application and a separate Python-based backend API, backed by a vector database (Pinecone) and a relational database (Supabase).

- **Frontend**: Modern Web Framework (Next.js, Vite/React, or HTML/CSS/JS)
- **Backend API**: Python FastAPI
- **Vector Database**: Pinecone (for document embeddings)
- **Relational Database & Auth**: Supabase (for structured data, chat memory, and user authentication)
- **LLM Provider**: OpenRouter (using `openai/gpt-4o-mini`)
- **Deployment**: Vercel (Monorepo setup using Serverless functions for the Python API)

---

## 2. Frontend Design

**Responsibilities:**
- Provide a rich, modern, and responsive user interface.
- Handle user authentication (Student and Parent accounts).
- Provide a chat interface for the RAG chatbot.
- Communicate with the backend via REST API calls.

**Key Components:**
- **Landing Page**: General school information.
- **Chatbot Interface**: A Gradio Chat UI embedded directly via an `iframe`. The Gradio app is mounted onto the FastAPI backend.
- **Authentication Flow**: Login screens connecting to Supabase Auth.

---

## 3. Backend API Design (FastAPI)

**Responsibilities:**
- Serve as the intermediary between the frontend, the LLM, and the databases.
- Handle chat requests and formulate prompts with context.
- Manage tool calling (Function Calling) for the LLM to access relational data.

**Core Endpoints:**
- `POST /api/chat` (or `/chat` in dev)
  - **Payload**: `{ "message": "string", "user_id": "string" }`
  - **Response**: `{ "reply": "string" }`

---

## 4. RAG & Memory System

The AI capability uses Retrieval-Augmented Generation (RAG) combined with persistent user memory.

### 4.1. Semantic Retrieval (Vector Search)
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Chunking Strategy**: Semantic chunking using `RecursiveCharacterTextSplitter` (chunk size: 400, overlap: 50).
- **Storage**: Pinecone. The text documents (fees policy, textbooks info, school policies, etc.) are embedded and queried to provide context for the LLM.

### 4.2. Tool Calling (Database Queries)
- The backend equips the LLM with tool calling capabilities to query structured data from Supabase.
- E.g., `get_db_data(table_name)` retrieves rows from specific tables like `fees` or `textbooks` when the user asks specific structured questions.

### 4.3. Persistent Memory
- User conversations are saved in Supabase (`chat_history` table).
- The chat history is retrieved using the `user_id` to maintain conversation context over multiple sessions.

---

## 5. Database Schema (Supabase)

### 5.1. Relational Tables
- **fees**: `id`, `grade`, `annual_fee`, `tuition_fee`, `created_at`
- **textbooks**: `id`, `grade`, `available`, `notes`, `created_at`
- **chat_history**: `id`, `user_id` (UUID), `role` ('user' or 'assistant'), `message`, `created_at`

### 5.2. Security & Authentication
- **Row Level Security (RLS)** is enabled on the `chat_history` table.
- **Policy**: `auth.uid() = user_id`. This ensures users can only access and modify their own conversation histories.
- Default users expected: `student@abcschool.com` and `parent@abcschool.com`.

---

## 6. Deployment Architecture

**Platform**: Vercel
**Structure**: Monorepo combining both frontend and backend.

- `vercel.json` coordinates the build process:
  - The Python FastAPI backend uses `@vercel/python` and is served as serverless functions.
  - The Next.js frontend uses `@vercel/next` (or static builds for React).
  - API requests starting with `/api/` are routed to the Python backend, while all other routes go to the frontend.
