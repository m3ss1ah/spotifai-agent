import os
import time
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from auth import generate_auth_url, exchange_code_for_tokens, refresh_access_token
from spotify import (
    get_user_profile, get_user_top_tracks, get_user_top_artists,
    get_user_playlists, create_playlist, get_recommendations, 
    add_tracks_to_playlist, get_playlist_tracks
)
from ai import SpotifyAIAssistant
from db import init_db, get_user, get_user_by_spotify_id, create_or_update_user, cache_user_stats, get_cached_stats
from models.user import TokenResponse, PlaylistCreate, BlendRequest, AIRequest
from utils.stats import extract_genres_from_artists, calculate_similarity_score, deduplicate_tracks, merge_playlists, calculate_listening_stats

load_dotenv()

# Initialize database
init_db()

# FastAPI app
app = FastAPI(
    title="Spotify AI Assistant",
    description="Spotify-connected AI assistant with LLaMA 3.2",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI assistant
ai_assistant = SpotifyAIAssistant()

# ============================================================================
# AUTH ENDPOINTS
# ============================================================================

@app.get("/auth/login")
async def login():
    """
    Generate Spotify OAuth login URL with PKCE.
    Frontend redirects user to this URL to start authorization flow.
    
    Returns:
        auth_url: URL to redirect user to Spotify login
        state: State parameter for CSRF protection (frontend should track this)
    """
    try:
        auth_url, state = generate_auth_url()
        return {
            "auth_url": auth_url,
            "state": state
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/auth/callback")
async def callback(code: str = Query(...), state: str = Query(...)):
    """
    Handle Spotify OAuth callback.
    Receives authorization code and exchanges it for access/refresh tokens.
    Frontend should redirect to /callback with code and state from Spotify.
    
    Query Parameters:
        code: Authorization code from Spotify
        state: State parameter for CSRF validation
        
    Returns:
        access_token: Token to make Spotify API calls
        refresh_token: Token to refresh access_token when expired
        user_id: Our database user ID
        expires_in: Token expiration time in seconds
    """
    try:
        # Exchange code for tokens using PKCE
        tokens = await exchange_code_for_tokens(code, state)
        
        # Get user profile from Spotify
        profile = await get_user_profile(tokens["access_token"])
        
        # Store/update user in database
        user_data = {
            "spotify_id": profile["spotify_id"],
            "access_token": tokens["access_token"],
            "refresh_token": tokens.get("refresh_token"),
            "token_expires_at": tokens.get("expires_at"),
            "display_name": profile["display_name"],
            "email": profile["email"],
            "followers": profile["followers"],
            "profile_url": profile["profile_url"],
            "image_url": profile["image_url"],
            "plan_type": profile["plan_type"]
        }
        
        user_id = create_or_update_user(user_data)
        
        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens.get("refresh_token"),
            "user_id": user_id,
            "expires_in": tokens.get("expires_in", 3600),
            "token_type": "Bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")

@app.post("/auth/refresh")
async def refresh(refresh_token: str = Body(..., embed=True)):
    """
    Refresh access token using refresh token.
    Called when access token expires.
    
    Body:
        refresh_token: Valid refresh token
        
    Returns:
        access_token: New access token
        expires_in: Token expiration time in seconds
    """
    try:
        tokens = await refresh_access_token(refresh_token)
        return {
            "access_token": tokens["access_token"],
            "expires_in": tokens.get("expires_in", 3600),
            "token_type": "Bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Token refresh failed: {str(e)}")

# ============================================================================
# USER ENDPOINTS
# ============================================================================

@app.get("/user/profile")
async def get_profile(user_id: str = Query(...)):
    """
    Get user profile and stats.
    Aggregates: profile info, top tracks, top artists, top genres, listening stats
    
    Query Parameters:
        user_id: User ID from our database
        
    Returns:
        User profile with all stats
    """
    try:
        user = get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if access token is expired
        if user["token_expires_at"] and user["token_expires_at"] < time.time():
            if user["refresh_token"]:
                tokens = await refresh_access_token(user["refresh_token"])
                user["access_token"] = tokens["access_token"]
                user["token_expires_at"] = tokens.get("expires_at")
            else:
                raise HTTPException(status_code=401, detail="Token expired, please login again")
        
        # Fetch fresh stats from Spotify
        top_tracks = await get_user_top_tracks(user["access_token"], limit=20)
        top_artists = await get_user_top_artists(user["access_token"], limit=20)
        genres_with_counts = extract_genres_from_artists(top_artists)
        top_genres = [genre for genre, _ in genres_with_counts]
        
        listening_stats = calculate_listening_stats(top_tracks)
        
        # Cache stats
        stats = {
            "top_tracks": top_tracks,
            "top_artists": top_artists,
            "top_genres": top_genres,
            "listening_stats": listening_stats
        }
        cache_user_stats(user_id, stats)
        
        return {
            "id": user["id"],
            "spotify_id": user["spotify_id"],
            "display_name": user["display_name"],
            "email": user["email"],
            "followers": user["followers"],
            "profile_url": user["profile_url"],
            "image_url": user["image_url"],
            "plan_type": user["plan_type"],
            "top_tracks": top_tracks,
            "top_artists": top_artists,
            "top_genres": top_genres,
            "listening_stats": listening_stats
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# PLAYLIST ENDPOINTS
# ============================================================================

@app.get("/playlists")
async def list_playlists(user_id: str = Query(...)):
    """
    Get user's playlists from Spotify.
    
    Query Parameters:
        user_id: User ID
        
    Returns:
        List of user's playlists with metadata
    """
    try:
        user = get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        playlists = await get_user_playlists(user["access_token"])
        return {"playlists": playlists}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/playlists/create")
async def create_new_playlist(user_id: str = Query(...), playlist: PlaylistCreate = Body(...)):
    """
    Create a new Spotify playlist.
    
    Query Parameters:
        user_id: User ID
        
    Body:
        name: Playlist name
        description: Optional description
        public: Whether playlist is public
        
    Returns:
        Created playlist data
    """
    try:
        user = get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        new_playlist = await create_playlist(
            user["access_token"],
            user["spotify_id"],
            playlist.name,
            playlist.description or "",
            playlist.public
        )
        return new_playlist
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/playlists/{playlist_id}/tracks")
async def get_tracks(playlist_id: str, user_id: str = Query(...)):
    """
    Get all tracks in a playlist.
    
    Path Parameters:
        playlist_id: Spotify playlist ID
        
    Query Parameters:
        user_id: User ID
        
    Returns:
        List of tracks in playlist
    """
    try:
        user = get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        tracks = await get_playlist_tracks(user["access_token"], playlist_id)
        return {"tracks": tracks}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/playlists/{playlist_id}/add-tracks")
async def add_tracks(
    playlist_id: str,
    user_id: str = Query(...),
    track_uris: list = Body(..., embed=True)
):
    """
    Add tracks to a playlist.
    
    Path Parameters:
        playlist_id: Spotify playlist ID
        
    Query Parameters:
        user_id: User ID
        
    Body:
        track_uris: List of Spotify track URIs
        
    Returns:
        Success status
    """
    try:
        user = get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        await add_tracks_to_playlist(user["access_token"], playlist_id, track_uris)
        return {"success": True, "message": f"Added {len(track_uris)} tracks"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# BLEND ENDPOINTS (Multi-user)
# ============================================================================

@app.post("/blend")
async def create_blend(blend_request: BlendRequest = Body(...)):
    """
    Create a blend between two users.
    Analyzes similarity, combines top tracks, and suggests merged playlist.
    
    Body:
        user_id1: First user ID
        user_id2: Second user ID
        playlist_name: Optional name for merged playlist
        
    Returns:
        Similarity score, overlap analysis, and recommendations
    """
    try:
        user1 = get_user(blend_request.user_id1)
        user2 = get_user(blend_request.user_id2)
        
        if not user1 or not user2:
            raise HTTPException(status_code=404, detail="One or both users not found")
        
        # Get top artists for both users
        artists1 = await get_user_top_artists(user1["access_token"], limit=20)
        artists2 = await get_user_top_artists(user2["access_token"], limit=20)
        
        genres1 = extract_genres_from_artists(artists1)
        genres2 = extract_genres_from_artists(artists2)
        
        genre_list1 = [g[0] for g in genres1[:10]]
        genre_list2 = [g[0] for g in genres2[:10]]
        
        # Calculate similarity
        similarity_score = calculate_similarity_score(genre_list1, genre_list2)
        
        # Get recommendations based on both users
        seed_artists1 = [a["id"] for a in artists1[:3]]
        seed_artists2 = [a["id"] for a in artists2[:2]]
        seed_genres = list(set(genre_list1[:3] + genre_list2[:2]))
        
        recommendations = await get_recommendations(
            user1["access_token"],
            seed_artists=seed_artists1 + seed_artists2,
            seed_genres=seed_genres,
            limit=30
        )
        
        return {
            "user1": user1["display_name"],
            "user2": user2["display_name"],
            "similarity_score": round(similarity_score, 2),
            "shared_genres": list(set(genre_list1) & set(genre_list2)),
            "user1_unique_genres": [g for g in genre_list1 if g not in genre_list2],
            "user2_unique_genres": [g for g in genre_list2 if g not in genre_list1],
            "recommendations": recommendations
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# AI ENDPOINTS
# ============================================================================

@app.post("/ai/playlist")
async def generate_playlist(ai_request: AIRequest = Body(...)):
    """
    Generate playlist name and recommendations using AI.
    
    Body:
        user_id: User ID
        prompt: User's request (e.g., "I want a focus playlist")
        context: Optional context data
        
    Returns:
        Generated playlist name and track recommendations
    """
    try:
        user = get_user(ai_request.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get user's top artists for seed data
        artists = await get_user_top_artists(user["access_token"], limit=10)
        genres = extract_genres_from_artists(artists)
        
        # Generate playlist name using AI
        mood = ai_request.context.get("mood") if ai_request.context else None
        playlist_name = await ai_assistant.generate_playlist_name(
            [g[0] for g in genres[:5]],
            mood
        )
        
        # Get recommendations
        seed_artists = [a["id"] for a in artists[:5]]
        seed_genres = [g[0] for g in genres[:5]]
        
        recommendations = await get_recommendations(
            user["access_token"],
            seed_artists=seed_artists,
            seed_genres=seed_genres,
            limit=30
        )
        
        return {
            "playlist_name": playlist_name,
            "description": f"AI-generated playlist based on your taste",
            "recommendations": recommendations,
            "seed_artists": [a["name"] for a in artists[:3]],
            "seed_genres": [g[0] for g in genres[:3]]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/mood")
async def analyze_mood(ai_request: AIRequest = Body(...)):
    """
    Analyze user's listening mood.
    
    Body:
        user_id: User ID
        prompt: Optional custom prompt
        
    Returns:
        Mood analysis from AI
    """
    try:
        user = get_user(ai_request.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get user's top data
        top_tracks = await get_user_top_tracks(user["access_token"], limit=10)
        top_artists = await get_user_top_artists(user["access_token"], limit=10)
        
        # Analyze mood with AI
        mood_analysis = await ai_assistant.analyze_mood(top_tracks, top_artists)
        
        return {
            "mood": mood_analysis,
            "top_tracks": top_tracks[:5],
            "top_artists": [a["name"] for a in top_artists[:5]]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/fix")
async def fix_playlist(ai_request: AIRequest = Body(...)):
    """
    Analyze and suggest improvements for a playlist.
    
    Body:
        user_id: User ID
        prompt: Playlist name to analyze
        
    Returns:
        Playlist analysis and improvement suggestions
    """
    try:
        user = get_user(ai_request.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Use prompt as playlist name to look up
        playlist_name = ai_request.prompt
        
        # Get user's playlists to find the one
        playlists = await get_user_playlists(user["access_token"])
        matching_playlist = next(
            (p for p in playlists if p["name"].lower() == playlist_name.lower()),
            None
        )
        
        if not matching_playlist:
            raise HTTPException(status_code=404, detail=f"Playlist '{playlist_name}' not found")
        
        # Get playlist tracks
        tracks = await get_playlist_tracks(user["access_token"], matching_playlist["id"])
        
        # Analyze with AI
        analysis = await ai_assistant.fix_playlist(playlist_name, tracks)
        
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/summary")
async def generate_summary(ai_request: AIRequest = Body(...)):
    """
    Generate a taste summary for the user.
    
    Body:
        user_id: User ID
        
    Returns:
        Personalized music taste summary
    """
    try:
        user = get_user(ai_request.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get user's top data
        top_tracks = await get_user_top_tracks(user["access_token"], limit=15)
        top_artists = await get_user_top_artists(user["access_token"], limit=15)
        genres = extract_genres_from_artists(top_artists)
        top_genres = [g[0] for g in genres]
        
        # Generate summary with AI
        summary = await ai_assistant.generate_taste_summary(top_tracks, top_artists, top_genres)
        
        return {
            "summary": summary,
            "top_artists": [a["name"] for a in top_artists[:5]],
            "top_genres": top_genres[:10],
            "taste_profile": {
                "diversity": len(set(top_genres)),
                "top_track": top_tracks[0]["name"] if top_tracks else "N/A",
                "top_artist": top_artists[0]["name"] if top_artists else "N/A"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "Spotify AI Assistant",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
