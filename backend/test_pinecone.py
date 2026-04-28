import os
from dotenv import load_dotenv
from pinecone import Pinecone
from huggingface_hub import InferenceClient

load_dotenv(dotenv_path="../.env")

PINECONE_KEY = os.getenv("PINECONE_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
INDEX_NAME = "school-chatbot"

pc = Pinecone(api_key=PINECONE_KEY)
index = pc.Index(INDEX_NAME)
hf_client = InferenceClient(token=HF_TOKEN)

try:
    print("Testing embedding...")
    emb = hf_client.feature_extraction("when are the exams scheduled?", model="sentence-transformers/all-MiniLM-L6-v2")
    
    # Handle the fact that InferenceClient.feature_extraction might return a list of lists or something weird
    import numpy as np
    emb_list = np.array(emb).tolist()
    
    # If it's a list of lists (e.g., shape [1, 384] or [384]), flatten it if needed
    if isinstance(emb_list[0], list):
        print(f"Warning: It is a list of lists, shape: {len(emb_list)}x{len(emb_list[0])}")
        emb_list = emb_list[0]
        
    print(f"Embedding length: {len(emb_list)}")
    
    print("Testing Pinecone...")
    res = index.query(vector=emb_list, top_k=3, include_metadata=True)
    print("Matches:")
    for m in res["matches"]:
        print("-", m["metadata"]["text"])
except Exception as e:
    import traceback
    traceback.print_exc()
