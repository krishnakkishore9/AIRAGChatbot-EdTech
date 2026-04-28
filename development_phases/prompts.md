# AI-Powered School Website + RAG Chatbot: Development Prompts

This document contains a series of actionable prompts structured around the project's development phases. These prompts can be copy-pasted to an AI assistant to systematically build the application according to the `design.md` architecture.

## Phase 1: Project Setup & Environment Configuration

**Prompt 1.1: Initialize Directories and Files**
> "Create the foundational directory structure for a monorepo setup for an AI-powered school platform. Create a `backend/` folder and a `frontend/` folder. Inside `backend/`, create a `data/docs/` folder for document storage. Also, create a `.env` file in the project root with placeholders for the following keys: `OPENROUTER_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`, `PINECONE_KEY`, and `PINECONE_ENV`."

**Prompt 1.2: Backend Dependencies and Vercel Setup**
> "In the `backend/` directory, create a `requirements.txt` file that includes `fastapi`, `uvicorn`, `pinecone-client`, `sentence-transformers`, `supabase`, `requests`, `python-dotenv`, `langchain`, and `langchain-text-splitters`. Then, at the project root, create a `vercel.json` file to configure the monorepo deployment. Configure the routes so that any request to `/api/*` is routed to the Python backend as Serverless Functions using `@vercel/python`, and all other requests go to the frontend using `@vercel/next` or static routing."

---

## Phase 2: Database & Authentication Setup (Supabase)

**Prompt 2.1: Supabase Schema Creation**
> "Write the SQL scripts required to create our Supabase relational tables:
> 1. `fees`: columns `id`, `grade`, `annual_fee`, `tuition_fee`, `created_at`.
> 2. `textbooks`: columns `id`, `grade`, `available`, `notes`, `created_at`.
> 3. `chat_history`: columns `id`, `user_id` (UUID), `role` (user/assistant), `message`, `created_at`.
> Provide the exact queries I need to execute in the Supabase SQL Editor."

**Prompt 2.2: RLS Policies and Authentication**
> "Provide the SQL commands to enable Row Level Security (RLS) on the `chat_history` table in Supabase. Create a policy that restricts users to only be able to `SELECT` and `INSERT` rows where `auth.uid() = user_id`. Next, provide step-by-step instructions on how to enable Email/Password authentication in the Supabase dashboard and create two test user accounts: `student@abcschool.com` and `parent@abcschool.com`."

---

## Phase 3: Vector Knowledge Base Setup (Pinecone)

**Prompt 3.1: Vector DB Upload Script**
> "Write a Python script `backend/upload_to_pinecone.py` that reads all text files located in the `backend/data/docs/` directory. The script should use LangChain's `RecursiveCharacterTextSplitter` with a chunk size of 400 and an overlap of 50 to chunk the documents. Use `SentenceTransformer("all-MiniLM-L6-v2")` to generate embeddings for these chunks. Finally, write the logic to connect to Pinecone (using the `school-chatbot` index) and upsert the generated vectors along with metadata about the source document."

---

## Phase 4: Backend API & RAG Implementation (FastAPI)

**Prompt 4.1: FastAPI Setup, Gradio, and Supabase Tooling**
> "Create the base FastAPI application in `backend/main.py`. Define a `POST /api/chat` endpoint that expects a Pydantic payload containing `message` (string) and `user_id` (UUID string). Create a simple Gradio ChatInterface and use `gr.mount_gradio_app()` to mount it onto the FastAPI app at the `/chat-ui` route. Furthermore, write a helper function `get_db_data(table_name)` that uses the Supabase Python client to query and retrieve all rows from the specified table. This function will be used as a data-retrieval tool for the LLM."

**Prompt 4.2: RAG Logic and Memory Integration**
> "Create a file named `backend/rag_chatbot.py`. Implement the following functionalities:
> 1. Embed an incoming user query and search the Pinecone index to retrieve relevant semantic chunks.
> 2. Query the Supabase `chat_history` table to fetch the last 5 messages for the given `user_id` to provide conversation history.
> 3. Create a function to save the new user query and the resulting assistant reply back into the `chat_history` table.
> Combine the retrieved Pinecone documents, chat history, and any relational data from Supabase to construct a cohesive context block."

**Prompt 4.3: LLM Orchestration via OpenRouter**
> "Using the OpenRouter API (`openai/gpt-4o-mini`), write the logic inside `rag_chatbot.py` to formulate the final prompt. Pass the system instructions, the retrieved context (History, Docs, DB Data), and the user's current message to the OpenRouter completion endpoint. Return the AI's generated `reply` back to the `/api/chat` endpoint in `main.py`."

---

## Phase 5: Frontend Development (Next.js/React)

**Prompt 5.1: Frontend App Initialization and UI**
> "Initialize a modern frontend project (Next.js or Vite React) in the `frontend/` directory. Design and implement a premium, responsive landing page for the school. Include a Chat Interface component that simply embeds the backend's Gradio app via an `iframe` pointing to the `/chat-ui` route."

**Prompt 5.2: Authentication and Backend Integration**
> "Integrate the Supabase Auth client into the frontend application. Implement login screens for students and parents, ensuring that the authenticated user's session and UUID are securely maintained. Finally, connect the Chat Interface to the backend by configuring it to send `POST` requests to the `/api/chat` endpoint, making sure to include both the user's `message` and their authenticated `user_id` in the request body."

---

## Phase 6: Testing & Vercel Deployment

**Prompt 6.1: Local Testing Instructions**
> "Provide a brief guide on how to test the system locally end-to-end. Include the commands to start the FastAPI server (`uvicorn`) and the frontend development server. List the key features I should manually verify, such as logging in, asking document-based questions, verifying memory retention across page reloads, and asking questions requiring database data (e.g., fees)."

**Prompt 6.2: Vercel Deployment Steps**
> "Write a step-by-step checklist to deploy this monorepo architecture to Vercel. Include how to verify the `vercel.json` routing configuration, how to properly inject the environment variables (Supabase, Pinecone, OpenRouter) into the Vercel dashboard, and how to validate that the Serverless Functions (Python API) and static frontend assets are functioning correctly in production."
