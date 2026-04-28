# Phase 3: Vector Knowledge Base Setup (Pinecone)

**Goal:** Create the vector index and populate it with semantic chunks from the school's document files.

## Steps:
1. **Pinecone Index Creation**
   - Create an index named `school-chatbot` in Pinecone with the appropriate dimensions for `all-MiniLM-L6-v2` (384 dimensions).
2. **Document Preparation**
   - Add the raw text files (`fees_policy.txt`, `textbooks_info.txt`, `school_policies.txt`, `holidays_schedule.txt`, `exam_schedule.txt`) into `backend/data/docs/`.
3. **Upload Script Implementation**
   - Implement `backend/upload_to_pinecone.py`.
   - Use `RecursiveCharacterTextSplitter` from LangChain for semantic chunking (chunk size: 400, overlap: 50).
   - Use `SentenceTransformer("all-MiniLM-L6-v2")` to generate embeddings.
4. **Populate Pinecone**
   - Run the upload script to process all documents and upsert the vectors with metadata to Pinecone.
