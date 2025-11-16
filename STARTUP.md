# 🚀 STARTUP GUIDE - Spotify AI Assistant

This guide walks you through setting up and running the Spotify AI Assistant.

## ⏱️ Setup Time: ~15-20 minutes

---

## STEP 1: Prerequisites Check ✅

Before starting, ensure you have:

- [x] Python 3.9+ installed
- [x] Node.js 16+ installed
- [x] Spotify Developer account (free at developer.spotify.com)
- [x] Ollama installed (https://ollama.ai)
- [x] LLaMA 3.2 model pulled: `ollama pull llama3.2`

---

## STEP 2: Get Spotify Credentials 🎵

1. Visit https://developer.spotify.com/dashboard
2. Log in with Spotify account (create free if needed)
3. Create a new app (accept terms)
4. Copy **Client ID** and **Client Secret**
5. Go to "Edit Settings"
6. Add Redirect URI: `http://127.0.0.1:3000/callback`
7. Save

---

## STEP 3: Configure Backend 🔧

### Windows PowerShell:

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env

# Edit .env (open in notepad)
notepad .env
```

### Edit `.env` file:
```
SPOTIFY_CLIENT_ID=<your_client_id>
SPOTIFY_CLIENT_SECRET=<your_client_secret>
SPOTIFY_REDIRECT_URI=http://127.0.0.1:3000/callback
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

---

## STEP 4: Start Ollama 🤖

**In a NEW terminal/PowerShell window:**

```powershell
ollama serve
```

This runs the LLaMA model server on `http://localhost:11434`

**Wait for:** `Listening on 127.0.0.1:11434`

---

## STEP 5: Start Backend 🚀

**In ANOTHER new terminal:**

```powershell
# Navigate to backend if not there
cd backend

# Activate venv
.\venv\Scripts\activate

# Start FastAPI server
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Wait for:** `Application startup complete`

Backend ready at: `http://127.0.0.1:8000`

---

## STEP 6: Start Frontend ⚡

**In ANOTHER new terminal:**

```powershell
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Start Vite dev server
npm run dev
```

**Wait for:** `Local: http://127.0.0.1:3000`

---

## STEP 7: Open Application 🎧

1. **Open browser** to `http://127.0.0.1:3000`
2. Click **"🎵 Login with Spotify"**
3. Authorize the app
4. **Enjoy! 🎉**

---

## 🎯 Feature Walkthrough

### Dashboard
- View your profile, followers, plan
- See top tracks with popularity scores
- Listening statistics

### Stats
- Top 20 artists with genres
- Top 15 genres as tags
- Detailed listening insights
- Full top tracks list

### Playlists
- Create new playlists
- View all your playlists
- See tracks in each playlist
- Add more tracks

### Blend
- Compare music taste with another user
- View shared genres
- See unique genres
- Get blend recommendations

### AI Agent (🤖)
- **Generate Playlist**: AI creates playlist name & recommendations
- **Analyze Mood**: AI describes your current listening mood
- **Fix Playlist**: AI suggests improvements for playlists
- **Taste Summary**: AI writes personalized music taste description

---

## 🔐 OAuth Flow (What Happens)

1. User clicks "Login with Spotify"
2. Browser redirects to Spotify login
3. User authorizes app → gets code
4. Code sent to backend
5. Backend exchanges code for access token (PKCE)
6. User data fetched from Spotify
7. Stored in local SQLite database
8. User logged in, token in localStorage

**No passwords stored!** Only OAuth tokens (can be revoked anytime)

---

## ⚙️ Terminal Windows You Should Have Open

```
Terminal 1: Ollama
$ ollama serve
→ http://localhost:11434

Terminal 2: Backend
$ python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
→ http://127.0.0.1:8000

Terminal 3: Frontend
$ npm run dev
→ http://127.0.0.1:3000
```

---

## 🆘 Troubleshooting

### "OAuth failed" / "Invalid redirect_uri"
- Verify exact redirect URI in Spotify dashboard
- Must be: `http://127.0.0.1:3000/callback`

### "Connection refused" to Ollama
- Is ollama running? Check terminal 1
- Run: `ollama serve`
- LLaMA 3.2 pulled? Run: `ollama pull llama3.2`

### "Cannot GET /callback"
- Backend not running? Check terminal 2
- Frontend trying to call backend?
- CORS error? Check browser console

### Database errors
- Delete `spotify_ai.db` in backend folder
- Restart backend server

### Python import errors
- Venv activated? (should see `(venv)` in terminal)
- Dependencies installed? `pip install -r requirements.txt`

### Node modules errors
- Delete `node_modules` folder and `package-lock.json`
- Run: `npm install` again

---

## 📊 API Docs

Once backend is running, visit:
`http://127.0.0.1:8000/docs`

Interactive API documentation with Swagger UI!

---

## 🎨 Customization Tips

### Change Colors
Edit any `.css` file:
- `#1DB954` = Spotify Green
- `#191414` = Dark Background
- `#282828` = Secondary

### Add New Pages
1. Create `frontend/src/pages/MyPage.jsx`
2. Create `frontend/src/pages/MyPage.css`
3. Add button in `Sidebar.jsx`
4. Import in `App.jsx`
5. Add route in switch statement

### Add Backend Endpoints
1. Add function in `main.py`
2. Add Pydantic model in `models/user.py` if needed
3. Call from frontend with axios

---

## 📚 Learn More

- Spotify API: https://developer.spotify.com/documentation/web-api
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- LangChain: https://python.langchain.com/

---

## 🎉 Success Checklist

- [ ] Ollama running and LLaMA 3.2 pulled
- [ ] Backend server started (port 8000)
- [ ] Frontend dev server started (port 3000)
- [ ] Spotify credentials in `.env`
- [ ] Can login with Spotify
- [ ] Can see profile data
- [ ] Can view stats
- [ ] AI features working

---

## 📞 Need Help?

1. Check browser console for errors (F12)
2. Check terminal outputs for stack traces
3. Verify `.env` file has all credentials
4. Make sure all three servers are running
5. Try deleting `spotify_ai.db` and restarting

---

Happy exploring! 🎵🤖✨
