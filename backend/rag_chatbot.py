import os
import requests
from dotenv import load_dotenv
from pinecone import Pinecone
from supabase import create_client
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv(dotenv_path="../.env")
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
PINECONE_KEY = os.getenv("PINECONE_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
INDEX_NAME = "school-chatbot"

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_KEY)
index = pc.Index(INDEX_NAME)

# Initialize Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize Hugging Face for Embeddings
hf_client = InferenceClient(token=HF_TOKEN)

def get_embedding(text):
    return hf_client.feature_extraction(text, model="sentence-transformers/all-MiniLM-L6-v2")

def retrieve_docs(query):
    try:
        emb = get_embedding(query)
        import numpy as np
        emb_list = np.array(emb).tolist()
        if isinstance(emb_list[0], list):
            emb_list = emb_list[0]
            
        res = index.query(vector=emb_list, top_k=3, include_metadata=True)
        return [m["metadata"]["text"] for m in res["matches"]]
    except Exception as e:
        print("Pinecone Retrieval Error:", e)
        return []

def get_db_data(table_name: str):
    """Fetch all rows from a specific Supabase table (e.g. 'fees', 'textbooks')."""
    try:
        res = supabase.table(table_name).select("*").execute()
        return res.data
    except Exception as e:
        print(f"Supabase DB Error ({table_name}):", e)
        return []

# MEMORY
def save_message(user_id, role, message):
    try:
        supabase.table("chat_history").insert({
            "user_id": user_id,
            "role": role,
            "message": message
        }).execute()
    except Exception as e:
        print("Error saving message (Check RLS policies):", e)

def get_history(user_id):
    try:
        res = supabase.table("chat_history") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .limit(5).execute()

        msgs = res.data[::-1] # Reverse to get chronological order
        history = ""
        for m in msgs:
            history += f"{m['role'].capitalize()}: {m['message']}\n"
        return history
    except Exception as e:
        print("Error getting history:", e)
        return ""

def generate_response(prompt):
    # A robust list of extremely reliable open-source models on Hugging Face
    fallback_models = [
        "Qwen/Qwen2.5-72B-Instruct",
        "mistralai/Mistral-Nemo-Instruct-2407",
        "microsoft/Phi-3-mini-4k-instruct"
    ]
    
    messages = [{"role": "user", "content": prompt}]
    
    for model in fallback_models:
        try:
            response = hf_client.chat_completion(
                model=model,
                messages=messages,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Warning: Model {model} failed: {str(e)}. Attempting fallback...")
            continue # Try the next model
            
    return "AI Generation Error: All fallback models are currently experiencing rate limits. Please try again in a few moments."

def get_bot_response(query, user_id):
    # 1. Fetch memory
    history = get_history(user_id)
    
    # 2. Fetch Vector DB Context (Documents)
    docs = retrieve_docs(query)
    
    # 3. Simple Tool Calling / Routing (Fetch Relational DB Context)
    db_data = [] 
    q_lower = query.lower()
    if "fee" in q_lower or "cost" in q_lower or "pay" in q_lower:
        db_data.extend(get_db_data("fees"))
    if "book" in q_lower or "text" in q_lower or "available" in q_lower:
        db_data.extend(get_db_data("textbooks"))
        
    prompt = f"""
You are a highly helpful and professional virtual assistant for a school. 
You must answer the user's question using ONLY the provided knowledge below.
If the information is not present in the knowledge, politely say so. DO NOT make up answers.

CRITICAL INSTRUCTION: The School Documents (such as policies, attendance rules, holidays, and exam schedules) are GENERIC and apply to ALL grades (1 through 10) unless explicitly stated otherwise. If a user asks about a policy or schedule for a specific grade (e.g. "policies for grade 5"), you MUST provide the general policies from the documents and inform them that these apply to all grades including theirs.

---
[Document Context (Vector DB)]
{docs}

---
[Database Context (SQL DB)]
{db_data}

---
[Chat History]
{history}

---
[User Question]
{query}
"""

    # 4. Generate Final Response
    reply = generate_response(prompt)

    # 5. Save State
    save_message(user_id, "user", query)
    save_message(user_id, "assistant", reply)

    return reply
