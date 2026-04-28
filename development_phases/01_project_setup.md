# Phase 1: Project Setup & Environment Configuration

**Goal:** Establish the foundational directory structure, configuration files, and environment variables for the monorepo.

## Steps:
1. **Directory Structure Initialization**
   - Create the `backend/` and `frontend/` folders.
   - Create `backend/data/docs/` for storing text documents.
2. **Environment Variables**
   - Create a `.env` file in the root/backend with the following keys:
     - `OPENROUTER_API_KEY`
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
     - `PINECONE_KEY`
     - `PINECONE_ENV`
3. **Backend Dependencies**
   - Create `backend/requirements.txt` containing: `fastapi`, `uvicorn`, `pinecone-client`, `sentence-transformers`, `supabase`, `requests`, `python-dotenv`, `langchain`, `langchain-text-splitters`.
   - Install dependencies in a virtual environment.
4. **Vercel Monorepo Setup**
   - Create `vercel.json` at the project root to configure build settings for both Python (Serverless Functions) and Next.js/React.
