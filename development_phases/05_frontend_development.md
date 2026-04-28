# Phase 5: Frontend Development (Next.js/React)

**Goal:** Create a modern, responsive web application with a chat interface and authentication.

## Steps:
1. **Frontend Initialization**
   - Initialize the Next.js or Vite React project in the `frontend/` directory.
   - Configure styles (Vanilla CSS, CSS Modules, or Tailwind) aiming for a premium, rich aesthetic.
2. **Authentication Flow**
   - Implement Login screens.
   - Integrate Supabase Auth client to authenticate students and parents.
   - Manage user sessions and securely store the authenticated UUID.
3. **Chat Interface**
   - Embed the Gradio Chat UI directly into the application using an `iframe` pointing to the backend's `/chat-ui` route.
4. **Backend Integration**
   - Configure API calls from the frontend chat UI to the backend `/api/chat` endpoint.
   - Ensure the authenticated user's UUID is passed securely in the payload.
