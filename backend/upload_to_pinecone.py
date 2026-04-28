import os
import uuid
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
import requests

# Load environment variables (from project root if needed)
load_dotenv(dotenv_path="../.env")
load_dotenv() # Fallback

PINECONE_KEY = os.getenv("PINECONE_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1") # default to something if not set
HF_TOKEN = os.getenv("HF_TOKEN")
INDEX_NAME = "school-chatbot"

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_KEY)

# Check if index exists, if not create it (dimension 384 for all-MiniLM-L6-v2)
if INDEX_NAME not in pc.list_indexes().names():
    print(f"Creating Pinecone index '{INDEX_NAME}'...")
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,
        metric='cosine',
        spec=ServerlessSpec(cloud='aws', region=PINECONE_ENV)
    )

index = pc.Index(INDEX_NAME)

from huggingface_hub import InferenceClient
client = InferenceClient(token=HF_TOKEN)

def get_embedding(text):
    embeddings = client.feature_extraction(text, model="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings

def upload(folder="data/docs/"):
    # Using a semantic chunker that respects word and paragraph boundaries
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )

    print(f"Reading files from {folder}...")
    for file in os.listdir(folder):
        if not file.endswith(".txt"):
            continue
            
        file_path = os.path.join(folder, file)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Split text semantically
        chunks = text_splitter.split_text(text)
        print(f"Chunked {file} into {len(chunks)} chunks.")

        vectors = []
        for i, c in enumerate(chunks):
            emb = get_embedding(c)
            # Generate a unique ID for each chunk
            chunk_id = f"{file}_{i}_{uuid.uuid4().hex[:6]}"
            vectors.append((chunk_id, emb, {"text": c, "source": file}))
            
        if vectors:
            index.upsert(vectors)
            print(f"Successfully upserted {len(vectors)} vectors for {file}.")

if __name__ == "__main__":
    # Ensure script can be run from the backend/ directory
    docs_folder = "data/docs/"
    if not os.path.exists(docs_folder):
        # Fallback if run from root
        docs_folder = "backend/data/docs/"
        
    upload(docs_folder)
    print("Upload complete!")
