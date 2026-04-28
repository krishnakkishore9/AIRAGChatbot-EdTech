# Phase 6: Testing & Vercel Deployment

**Goal:** Verify the system end-to-end and deploy the monorepo to Vercel.

## Steps:
1. **Local End-to-End Testing**
   - Start the FastAPI backend locally (`uvicorn main:app --port 8000`).
   - Start the frontend dev server.
   - Test login, generic chat questions, memory retention across refreshes, and structured data queries (e.g., fees).
2. **Vercel Configuration Verification**
   - Verify `vercel.json` routing rules properly map `/api/*` to the Python backend and `/*` to the frontend.
3. **Environment Setup on Vercel**
   - Push the repository to GitHub.
   - Import the project into Vercel.
   - Add all environment variables (Supabase, Pinecone, OpenRouter) to the Vercel project settings.
4. **Deploy & Validate**
   - Trigger the deployment.
   - Verify both frontend asset delivery and Serverless Function API execution in the production environment.
