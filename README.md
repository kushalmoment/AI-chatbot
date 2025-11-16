# AI Chatbot Project

This is a full-stack AI chatbot application built with Flask (backend) and React (frontend), using Google's Gemini API for AI responses and Firebase for data storage.

## Features

- AI-powered chat using Gemini API
- User authentication via Firebase
- Chat history storage
- Admin dashboard
- Responsive UI

## Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   cd frontend && npm install
   ```
3. Set up environment variables in `backend/.env`:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   FIREBASE_CRED_PATH=backend/firebase-key.json
   FIREBASE_PROJECT_ID=your_firebase_project_id
   GENERATIVE_MODEL=gemini-2.5-flash
   ```
4. Run the backend:
   ```bash
   python backend/run_server.py
   ```
5. Run the frontend:
   ```bash
   cd frontend && npm start
   ```

## Deployment Options

### Option 1: Railway (Recommended - Most Reliable)

1. Sign up at [railway.app](https://railway.app)
2. Connect your repository
3. Railway will auto-detect Python and use the `railway.toml` configuration
4. Set environment variables in Railway dashboard:
   - `GEMINI_API_KEY`
   - `FIREBASE_PROJECT_ID`
   - `GENERATIVE_MODEL=gemini-2.5-flash`
5. Upload your `backend/firebase-key.json` file to Railway
6. Deploy!

### Option 2: Render

1. Sign up for a free account at [render.com](https://render.com)
2. Connect your GitHub repository
3. Use the `render.yaml` file for configuration
4. Set environment variables in Render dashboard
5. Deploy!

### Option 3: Vercel (Frontend + Backend)

1. Sign up at [vercel.com](https://vercel.com)
2. Use the `vercel.json` configuration
3. Set environment variables
4. Deploy!

## Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key
- `FIREBASE_CRED_PATH`: Path to Firebase service account JSON
- `FIREBASE_PROJECT_ID`: Your Firebase project ID
- `GENERATIVE_MODEL`: Gemini model to use (default: gemini-2.5-flash)

## API Endpoints

- `GET /api/chat/test`: Test API connectivity
- `POST /api/chat/message`: Send chat message
- `GET /`: Serve frontend
- `GET /static/*`: Serve static files

## Technologies Used

- **Backend**: Flask, Waitress, Google Generative AI, Firebase Admin
- **Frontend**: React, TypeScript
- **Database**: Firebase Firestore
- **Deployment**: Render/Railway/Vercel
