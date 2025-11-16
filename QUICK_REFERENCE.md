# 📋 QUICK REFERENCE

## 🏃 Fast Start (Copy-Paste Commands)

### Terminal 1 - Ollama
```powershell
ollama serve
```

### Terminal 2 - Backend
```powershell
cd backend
.\venv\Scripts\activate
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Terminal 3 - Frontend
```powershell
cd frontend
npm run dev
```

### Terminal 4 - First Time Setup
```powershell
# Backend
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env with Spotify credentials

# Frontend
cd frontend
npm install
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `backend/main.py` | All API routes |
| `backend/auth.py` | OAuth + PKCE |
| `backend/spotify.py` | Spotify API calls |
| `backend/ai.py` | LLaMA AI logic |
| `backend/.env` | Credentials (CREATE THIS) |
| `frontend/src/App.jsx` | Main app component |
| `frontend/src/pages/` | Page components |
| `frontend/src/components/` | Reusable components |

---

## 🔗 URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://127.0.0.1:3000 | User interface |
| Backend | http://127.0.0.1:8000 | API server |
| API Docs | http://127.0.0.1:8000/docs | Swagger UI |
| Ollama | http://localhost:11434 | LLaMA model |

---

## 🎯 API Endpoints (Quick Reference)

### Auth
```
GET  /auth/login
GET  /auth/callback?code=XXX&state=XXX
POST /auth/refresh
```

### User
```
GET /user/profile?user_id=XXX
```

### Playlists
```
GET  /playlists?user_id=XXX
POST /playlists/create?user_id=XXX
GET  /playlists/{id}/tracks?user_id=XXX
POST /playlists/{id}/add-tracks?user_id=XXX
```

### Blend
```
POST /blend
{
  "user_id1": "xxx",
  "user_id2": "yyy",
  "playlist_name": "optional"
}
```

### AI
```
POST /ai/playlist
POST /ai/mood
POST /ai/fix
POST /ai/summary
```

---

## 🎨 Spotify Colors (Copy-Paste)

```css
/* Primary Green */
color: #1DB954;

/* Hover Green */
color: #1ed760;

/* Dark Background */
background-color: #191414;

/* Secondary Dark */
background-color: #282828;

/* Light Text */
color: #FFFFFF;

/* Dim Text */
color: #B3B3B3;
```

---

## 🐛 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Port 8000 in use | `netstat -ano \| findstr :8000` → kill process |
| Port 3000 in use | `netstat -ano \| findstr :3000` → kill process |
| Venv not working | Use: `python -m venv venv` not `virtualenv` |
| Module not found | Check venv activated + `pip install -r requirements.txt` |
| Ollama 404 | Start ollama: `ollama serve` |
| Database locked | Delete `spotify_ai.db` and restart |
| OAuth failed | Verify redirect URI in Spotify dashboard |

---

## 📦 Key Dependencies

### Backend
- fastapi (web framework)
- uvicorn (ASGI server)
- httpx (async HTTP)
- langchain (AI orchestration)
- langchain-ollama (Ollama integration)
- sqlite3 (database)

### Frontend
- react (UI framework)
- vite (build tool)
- axios (HTTP client)

---

## 💾 Environment Variables (.env)

```
# Required
SPOTIFY_CLIENT_ID=<from developer.spotify.com>
SPOTIFY_CLIENT_SECRET=<from developer.spotify.com>
SPOTIFY_REDIRECT_URI=http://127.0.0.1:3000/callback

# Optional (defaults)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
BACKEND_URL=http://127.0.0.1:8000
FRONTEND_URL=http://127.0.0.1:3000
DATABASE_URL=sqlite:///./spotify_ai.db
```

---

## 🔄 OAuth Flow (Simplified)

1. User clicks login button
2. Frontend requests auth URL from backend
3. Frontend redirects to Spotify
4. User authorizes
5. Spotify redirects to http://127.0.0.1:3000/callback?code=XXX&state=XXX
6. Frontend extracts code and state
7. Frontend sends to `/auth/callback`
8. Backend exchanges code for tokens (PKCE)
9. Backend fetches user profile
10. Returns tokens and user data
11. Frontend stores in localStorage
12. User logged in ✅

---

## 📊 Database Schema

### users
```sql
id TEXT PRIMARY KEY
spotify_id TEXT UNIQUE
access_token TEXT
refresh_token TEXT
token_expires_at REAL
display_name TEXT
email TEXT
followers INTEGER
profile_url TEXT
image_url TEXT
plan_type TEXT
```

### user_stats
```sql
id INTEGER PRIMARY KEY
user_id TEXT FOREIGN KEY
top_tracks TEXT (JSON)
top_artists TEXT (JSON)
top_genres TEXT (JSON)
listening_stats TEXT (JSON)
cached_at TIMESTAMP
```

### playlists
```sql
id TEXT PRIMARY KEY
user_id TEXT FOREIGN KEY
spotify_playlist_id TEXT
name TEXT
description TEXT
track_count INTEGER
public INTEGER
created_at TIMESTAMP
```

---

## 🚀 Deploy Checklist

- [ ] All .env variables set correctly
- [ ] Ollama running with LLaMA 3.2
- [ ] Backend running on 8000
- [ ] Frontend built: `npm run build`
- [ ] Database initialized
- [ ] Spotify OAuth credentials valid
- [ ] CORS allowed for frontend URL
- [ ] All API routes tested

---

## 📞 Debug Commands

```powershell
# Check if ports are open
netstat -ano | findstr :8000
netstat -ano | findstr :3000
netstat -ano | findstr :11434

# Kill process on port
# netstat -ano | findstr :PORT
# taskkill /PID <PID> /F

# Check Python venv
pip list

# Check Node packages
npm list

# Test API
curl http://127.0.0.1:8000/health

# Test Ollama
curl http://localhost:11434/api/tags
```

---

## 🎓 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/
- **Spotify API**: https://developer.spotify.com/documentation/web-api/reference
- **LangChain**: https://js.langchain.com/docs/
- **Ollama**: https://github.com/ollama/ollama

---

Made with ❤️ by the SpotiAI team
