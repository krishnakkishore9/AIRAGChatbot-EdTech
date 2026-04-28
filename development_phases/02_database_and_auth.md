# Phase 2: Database & Authentication Setup (Supabase)

**Goal:** Configure the relational database, table schemas, and user authentication to support user memory and structured data querying.

## Steps:
1. **Project Initialization in Supabase**
   - Create a new project in the Supabase dashboard.
   - Obtain the URL and API keys and update the `.env` file.
2. **Authentication Setup**
   - Enable Email/Password authentication.
   - Create test users: `student@abcschool.com` and `parent@abcschool.com`.
3. **Schema Creation**
   - Execute SQL scripts to create the `fees` table.
   - Execute SQL scripts to create the `textbooks` table.
   - Execute SQL scripts to create the `chat_history` table (for persistent user memory).
4. **Security & RLS (Row Level Security)**
   - Enable RLS on the `chat_history` table.
   - Create a policy allowing users to only `SELECT` and `INSERT` rows where `auth.uid() = user_id`.
