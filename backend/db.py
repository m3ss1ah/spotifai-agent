import sqlite3
import os
from datetime import datetime
from typing import Optional, Dict, Any

DATABASE_FILE = "spotify_ai.db"

def init_db():
    """Initialize database with required tables."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        spotify_id TEXT UNIQUE,
        access_token TEXT,
        refresh_token TEXT,
        token_expires_at REAL,
        display_name TEXT,
        email TEXT,
        followers INTEGER,
        profile_url TEXT,
        image_url TEXT,
        plan_type TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        top_tracks TEXT,
        top_artists TEXT,
        top_genres TEXT,
        listening_stats TEXT,
        cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS playlists (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        spotify_playlist_id TEXT,
        name TEXT,
        description TEXT,
        track_count INTEGER,
        public INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    conn.commit()
    conn.close()

def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user by ID."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    return dict(result) if result else None

def get_user_by_spotify_id(spotify_id: str) -> Optional[Dict[str, Any]]:
    """Get user by Spotify ID."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE spotify_id = ?", (spotify_id,))
    result = cursor.fetchone()
    conn.close()
    
    return dict(result) if result else None

def create_or_update_user(user_data: Dict[str, Any]) -> str:
    """Create or update user in database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    user_id = user_data.get("id", user_data.get("spotify_id"))
    
    cursor.execute("""
    INSERT OR REPLACE INTO users 
    (id, spotify_id, access_token, refresh_token, token_expires_at, 
     display_name, email, followers, profile_url, image_url, plan_type, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (
        user_id,
        user_data.get("spotify_id"),
        user_data.get("access_token"),
        user_data.get("refresh_token"),
        user_data.get("token_expires_at"),
        user_data.get("display_name"),
        user_data.get("email"),
        user_data.get("followers"),
        user_data.get("profile_url"),
        user_data.get("image_url"),
        user_data.get("plan_type")
    ))
    
    conn.commit()
    conn.close()
    
    return user_id

def cache_user_stats(user_id: str, stats: Dict[str, Any]):
    """Cache user statistics."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    import json
    cursor.execute("""
    INSERT INTO user_stats (user_id, top_tracks, top_artists, top_genres, listening_stats)
    VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        json.dumps(stats.get("top_tracks", [])),
        json.dumps(stats.get("top_artists", [])),
        json.dumps(stats.get("top_genres", [])),
        json.dumps(stats.get("listening_stats", {}))
    ))
    
    conn.commit()
    conn.close()

def get_cached_stats(user_id: str) -> Optional[Dict[str, Any]]:
    """Get cached user statistics."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT * FROM user_stats 
    WHERE user_id = ? 
    ORDER BY cached_at DESC LIMIT 1
    """, (user_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        import json
        return {
            "top_tracks": json.loads(result["top_tracks"]),
            "top_artists": json.loads(result["top_artists"]),
            "top_genres": json.loads(result["top_genres"]),
            "listening_stats": json.loads(result["listening_stats"])
        }
    
    return None
