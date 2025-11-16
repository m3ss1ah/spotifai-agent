# 🎧 Spotify AI Assistant

A full-stack application that combines Spotify's music data with LLaMA 3.2 AI to provide intelligent music recommendations, playlist analysis, and personalized music insights.

## 🌟 Features

### Spotify Integration
- **OAuth 2.0 + PKCE Authentication** - Secure login with Spotify
- **User Profile & Stats** - View followers, listening history, top tracks
- **Top Artists & Genres** - See your most-played artists and genres
- **Playlist Management** - Create, view, and manage playlists
- **Recommendations** - Get AI-powered track recommendations
- **Blend Feature** - Analyze music compatibility with other users

### AI Features (LLaMA 3.2)
- **Playlist Generator** - AI creates custom playlists based on your mood
- **Mood Analyzer** - Analyze your current listening mood
- **Playlist Fixer** - Get suggestions to improve existing playlists
- **Taste Summary** - AI generates personalized music taste analysis

### User Experience
- **Spotify Theme UI** - Dark green (#1DB954) and black (#191414) design
- **Animated Buttons** - Smooth hover effects and transitions
- **Card-based UI** - Clean, modern component design
- **Responsive Layout** - Works on desktop and mobile
- **Sidebar Navigation** - Easy access to all features

## 🧱 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **LangChain + Ollama** - Local LLaMA 3.2 integration
- **ChromaDB** - Vector database for embeddings
- **SQLite** - Lightweight database
- **HTTPX** - Async HTTP client for Spotify API
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI framework
- **Vite** - Fast build tool
- **Axios** - HTTP client
- **CSS3** - Styling with Spotify theme

## 📋 Prerequisites

1. **Python 3.9+** - For backend
2. **Node.js 16+** - For frontend
3. **Spotify Developer Account** - For OAuth credentials
4. **Ollama** - Local LLaMA model runner
5. **LLaMA 3.2 Model** - Downloaded in Ollama

## 🚀 Quick Start

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Spotify credentials
```

### 2. Spotify OAuth Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Accept terms and create
4. Get your **Client ID** and **Client Secret**
5. Add Redirect URI: `http://127.0.0.1:3000/callback`
6. Add these to your `.env` file

### 3. Ollama Setup

```bash
# Download and install Ollama from https://ollama.ai
# Pull LLaMA 3.2 model
ollama pull llama3.2

# Start Ollama service (runs on http://localhost:11434)
ollama serve
```

### 4. Start Backend

```bash
# From backend directory with venv activated
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Backend will be available at `http://127.0.0.1:8000`

### 5. Frontend Setup

```bash
# In a new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at `http://127.0.0.1:3000`

## 📁 Project Structure

```
spotifai-agent/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── auth.py              # Spotify OAuth + PKCE
│   ├── spotify.py           # Spotify API calls
│   ├── ai.py                # LLaMA AI assistant
│   ├── db.py                # SQLite database
│   ├── models/
│   │   └── user.py          # Pydantic models
│   ├── utils/
│   │   └── stats.py         # Statistics calculations
│   ├── chroma/              # Vector database
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── App.css
│       ├── pages/
│       │   ├── Login.jsx
│       │   ├── Dashboard.jsx
│       │   ├── Stats.jsx
│       │   ├── Playlists.jsx
│       │   ├── Blend.jsx
│       │   └── Agent.jsx
│       │   └── [respective CSS files]
│       └── components/
│           ├── Sidebar.jsx
│           ├── UserCard.jsx
│           └── [respective CSS files]
│
└── README.md
```

## 🔐 Security Features

- **OAuth 2.0 with PKCE** - Industry-standard authentication
- **Token Refresh** - Automatic access token refresh
- **State Validation** - CSRF protection on redirects
- **CORS Enabled** - Secure cross-origin requests
- **Secure Storage** - Tokens in localStorage with expiry tracking

## 🎨 Spotify Theme Colors

- **Primary Green**: `#1DB954`
- **Hover Green**: `#1ed760`
- **Background**: `#191414`
- **Secondary**: `#282828`
- **Text**: `#FFFFFF` / `#B3B3B3`

## 📡 API Endpoints

### Authentication
- `GET /auth/login` - Get OAuth URL
- `GET /auth/callback` - Handle OAuth callback
- `POST /auth/refresh` - Refresh access token

### User
- `GET /user/profile` - Get user profile & stats

### Playlists
- `GET /playlists` - List user playlists
- `POST /playlists/create` - Create playlist
- `GET /playlists/{id}/tracks` - Get playlist tracks
- `POST /playlists/{id}/add-tracks` - Add tracks

### Blend
- `POST /blend` - Create blend between users

### AI Features
- `POST /ai/playlist` - Generate playlist
- `POST /ai/mood` - Analyze mood
- `POST /ai/fix` - Fix playlist
- `POST /ai/summary` - Get taste summary

### Health
- `GET /health` - Health check

## 🧠 How AI Features Work

### Playlist Generation
Uses user's top artists and genres as seeds, then calls LLaMA to:
- Generate creative playlist name
- Explain the playlist concept
- Return Spotify recommendations

### Mood Analysis
Analyzes top 10 tracks and artists to determine:
- Current listening mood
- Music style preferences
- Emotional tone

### Playlist Fixer
Reviews playlist tracks and suggests:
- Theme/coherence analysis
- Track flow improvements
- Genre/tempo recommendations

### Taste Summary
Creates personalized description of:
- Overall music taste
- Top influences
- Listening patterns

## 🛠️ Development

### Adding New Features

1. **Backend**: Add route in `main.py`, logic in respective module
2. **Frontend**: Create component in `src/pages` or `src/components`
3. **Styling**: Add CSS file with component name
4. **API**: Update axios calls in frontend components

### Environment Variables

```
# Spotify OAuth
SPOTIFY_CLIENT_ID=your_id
SPOTIFY_CLIENT_SECRET=your_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:3000/callback

# LLaMA
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Server
BACKEND_URL=http://127.0.0.1:8000
FRONTEND_URL=http://127.0.0.1:3000

# Database
DATABASE_URL=sqlite:///./spotify_ai.db
```

## 📝 Notes

- Requires Ollama running with LLaMA 3.2 pulled
- Spotify API has rate limits - be mindful with requests
- First-time stats fetch may take a moment
- Playlists are created in user's Spotify account

## 🐛 Troubleshooting

**OAuth Error**: Verify redirect URI matches exactly in Spotify Dashboard
**Ollama Connection**: Make sure `ollama serve` is running
**Database Error**: Delete `spotify_ai.db` and restart backend
**CORS Error**: Check frontend/backend URLs in `.env`

## 📄 License

MIT License - See LICENSE file

## 🤝 Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

---

Built with ❤️ using FastAPI, React, and LLaMA
