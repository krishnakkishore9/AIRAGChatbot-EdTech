# Phase 6: Testing & Deployment Guide

Congratulations! You have successfully built a full-stack, AI-powered School Chatbot with a React frontend, FastAPI backend, Supabase Auth/Postgres, and a Pinecone Vector Database!

Follow these final steps to verify the application locally and deploy it seamlessly to the internet via Vercel.

---

## Part 1: Local End-to-End Testing

Before pushing to production, verify all core functionalities are working on your local machine.

### 1. Start the Servers
Open two terminal windows:

**Terminal 1: FastAPI Backend**
```bash
cd backend
python -m uvicorn main:app --port 8000
```

**Terminal 2: React Frontend**
```bash
cd frontend
npm run dev
```

### 2. Manual Verification Checklist
- [ ] **Landing Page:** Open `http://localhost:5173`. Verify the cinematic hero background and features grid load correctly.
- [ ] **Authentication:** Click "Login to Portal". Sign in with your parent or student test account. Verify you are redirected back to the landing page and the floating "Ask Nexus AI" button appears.
- [ ] **Chat UI:** Click the floating chat button. A sleek popup should appear showing your past chat history loaded from Supabase.
- [ ] **Vector AI (Pinecone):** Ask "When are the exams scheduled?" The AI should correctly answer based on the `school-documents` you uploaded to Pinecone.
- [ ] **Relational DB (Supabase):** Ask "What is the tuition fee for grade 8?" The AI should instantly look up the `fees` table and respond with the exact number.

---

## Part 2: Vercel Deployment

We have already correctly configured the `vercel.json` routing and the root `package.json` to handle this Python + Node.js monorepo automatically!

### Step 1: Push to GitHub
If you haven't already, push this entire folder to a new GitHub repository:
```bash
git init
git add .
git commit -m "Initial commit: AI School Chatbot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 2: Import into Vercel
1. Go to your [Vercel Dashboard](https://vercel.com/dashboard) and click **Add New... > Project**.
2. Select your newly created GitHub repository.
3. In the "Configure Project" screen, **leave the Framework Preset as "Other"** and **leave the Root Directory as "./"** (Do not change it to frontend). Vercel will read our custom `vercel.json` and build the frontend using the root `package.json`!

### Step 3: Inject Environment Variables
Before clicking Deploy, expand the **Environment Variables** section and copy-paste all the secrets from your local `.env` file!

**Required Variables:**
- `OPENROUTER_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`
- `PINECONE_KEY`
- `PINECONE_ENV`
- `HF_TOKEN`

*(Note: Vercel will automatically inject these into the Python backend!)*

### Step 4: Deploy!
1. Click **Deploy**.
2. Wait a few minutes. Vercel will automatically run `npm run build` in the frontend directory and package your FastAPI code into Serverless Functions.
3. Once complete, click the generated domains (e.g., `https://your-school-app.vercel.app`).

### Step 5: CORS Update (Crucial)
Because your frontend is now hosted on a real `https://...` domain, the FastAPI backend will block requests for security reasons until you add the new domain to your CORS policy!

1. Open `backend/main.py`.
2. Find the `origins` list at the top.
3. Add your new Vercel domain to the list:
```python
origins = [
    "http://localhost:5173",
    "https://your-school-app.vercel.app" # <-- Add your Vercel URL!
]
```
4. Push this one-line change to GitHub (`git add . && git commit -m "Update CORS" && git push`). Vercel will instantly redeploy, and your app is officially live to the world! 🎉
