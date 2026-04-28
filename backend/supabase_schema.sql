-- ==========================================
-- 1. Create Relational Tables
-- ==========================================

-- Fees Table
CREATE TABLE fees (
    id SERIAL PRIMARY KEY,
    grade INT NOT NULL,
    annual_fee INT NOT NULL,
    tuition_fee INT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Textbooks Table
CREATE TABLE textbooks (
    id SERIAL PRIMARY KEY,
    grade INT NOT NULL,
    available TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Chat History Table (Memory)
CREATE TABLE chat_history (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL, -- Ties directly to Supabase Auth UUID
    role TEXT CHECK (role IN ('user', 'assistant')) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- ==========================================
-- 2. Row Level Security (RLS) Policies
-- ==========================================

-- Enable RLS on the chat_history table
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;

-- Create policy to allow users to select and insert their own chat history
CREATE POLICY "Users can manage own chats"
ON chat_history
FOR ALL
USING (auth.uid() = user_id);

-- Note: We are not enabling RLS on `fees` or `textbooks` right now 
-- assuming they are read-only public knowledge base tables for the RAG agent. 
-- If they need to be protected, enable RLS and add public read policies:
-- ALTER TABLE fees ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY "Public read access" ON fees FOR SELECT USING (true);
