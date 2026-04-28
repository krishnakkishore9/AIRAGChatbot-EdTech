import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(token=HF_TOKEN)

try:
    embeddings = client.feature_extraction("Hello world", model="sentence-transformers/all-MiniLM-L6-v2")
    print("Success:", embeddings[:5])
except Exception as e:
    print("Error:", e)
