import httpx
import time
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import db

SPOTIFY_API_BASE = "https://api.spotify.com/v1"

async def get_user_profile(access_token: str) -> Dict[str, Any]:
    """
    Fetch user profile from Spotify API.
    
    Args:
        access_token: Valid Spotify access token
        
    Returns:
        User profile dictionary
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SPOTIFY_API_BASE}/me", headers=headers)
        response.raise_for_status()
        profile = response.json()
    
    image_url = None
    if profile.get("images") and len(profile["images"]) > 0:
        image_url = profile["images"][0]["url"]
    
    return {
        "spotify_id": profile["id"],
        "display_name": profile.get("display_name", "Unknown"),
        "email": profile.get("email", ""),
        "followers": profile.get("followers", {}).get("total", 0),
        "profile_url": profile.get("external_urls", {}).get("spotify", ""),
        "image_url": image_url,
        "plan_type": profile.get("product", "free")
    }

async def get_user_top_tracks(access_token: str, limit: int = 20, time_range: str = "medium_term") -> List[Dict[str, Any]]:
    """
    Fetch user's top tracks from Spotify.
    
    Args:
        access_token: Valid Spotify access token
        limit: Number of tracks to fetch (max 50)
        time_range: Time range ('short_term', 'medium_term', 'long_term')
        
    Returns:
        List of top tracks
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"limit": min(limit, 50), "time_range": time_range}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SPOTIFY_API_BASE}/me/top/tracks",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        data = response.json()
    
    tracks = []
    for item in data.get("items", []):
        tracks.append({
            "id": item["id"],
            "name": item["name"],
            "artists": [artist["name"] for artist in item.get("artists", [])],
            "album": item.get("album", {}).get("name", ""),
            "popularity": item.get("popularity", 0),
            "uri": item["uri"]
        })
    
    return tracks

async def get_user_top_artists(access_token: str, limit: int = 20, time_range: str = "medium_term") -> List[Dict[str, Any]]:
    """
    Fetch user's top artists from Spotify.
    
    Args:
        access_token: Valid Spotify access token
        limit: Number of artists to fetch (max 50)
        time_range: Time range ('short_term', 'medium_term', 'long_term')
        
    Returns:
        List of top artists with genres
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"limit": min(limit, 50), "time_range": time_range}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SPOTIFY_API_BASE}/me/top/artists",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        data = response.json()
    
    artists = []
    for item in data.get("items", []):
        artists.append({
            "id": item["id"],
            "name": item["name"],
            "genres": item.get("genres", []),
            "popularity": item.get("popularity", 0),
            "uri": item["uri"]
        })
    
    return artists

async def get_user_playlists(access_token: str, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Fetch user's playlists from Spotify.
    
    Args:
        access_token: Valid Spotify access token
        limit: Number of playlists to fetch (max 50)
        
    Returns:
        List of user playlists
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    playlists = []
    offset = 0
    
    async with httpx.AsyncClient() as client:
        while offset < limit:
            params = {"offset": offset, "limit": min(limit - offset, 50)}
            response = await client.get(
                f"{SPOTIFY_API_BASE}/me/playlists",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            for item in data.get("items", []):
                playlists.append({
                    "id": item["id"],
                    "name": item["name"],
                    "description": item.get("description", ""),
                    "track_count": item.get("tracks", {}).get("total", 0),
                    "public": item.get("public", False),
                    "uri": item["uri"]
                })
            
            offset += len(data.get("items", []))
            if not data.get("next"):
                break
    
    return playlists

async def create_playlist(access_token: str, user_id: str, name: str, description: str = "", public: bool = False) -> Dict[str, Any]:
    """
    Create a new playlist for the user.
    
    Args:
        access_token: Valid Spotify access token
        user_id: Spotify user ID
        name: Playlist name
        description: Playlist description
        public: Whether playlist is public
        
    Returns:
        Created playlist data
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "name": name,
        "public": public,
        "description": description
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SPOTIFY_API_BASE}/users/{user_id}/playlists",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        playlist = response.json()
    
    return {
        "id": playlist["id"],
        "name": playlist["name"],
        "description": playlist.get("description", ""),
        "uri": playlist["uri"]
    }

async def get_recommendations(access_token: str, seed_artists: List[str] = None, seed_genres: List[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Get Spotify recommendations based on seeds.
    
    Args:
        access_token: Valid Spotify access token
        seed_artists: List of artist IDs (max 5)
        seed_genres: List of genres (max 5)
        limit: Number of recommendations (max 100)
        
    Returns:
        List of recommended tracks
    """
    seed_artists = seed_artists or []
    seed_genres = seed_genres or []
    
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "seed_artists": ",".join(seed_artists[:5]),
        "seed_genres": ",".join(seed_genres[:5]),
        "limit": min(limit, 100)
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SPOTIFY_API_BASE}/recommendations",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        data = response.json()
    
    tracks = []
    for item in data.get("tracks", []):
        tracks.append({
            "id": item["id"],
            "name": item["name"],
            "artists": [artist["name"] for artist in item.get("artists", [])],
            "album": item.get("album", {}).get("name", ""),
            "uri": item["uri"]
        })
    
    return tracks

async def add_tracks_to_playlist(access_token: str, playlist_id: str, track_uris: List[str]) -> bool:
    """
    Add tracks to a playlist.
    
    Args:
        access_token: Valid Spotify access token
        playlist_id: Spotify playlist ID
        track_uris: List of track URIs (max 100 per request)
        
    Returns:
        Success status
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    
    async with httpx.AsyncClient() as client:
        for i in range(0, len(track_uris), 100):
            batch = track_uris[i:i+100]
            response = await client.post(
                f"{SPOTIFY_API_BASE}/playlists/{playlist_id}/tracks",
                headers=headers,
                json={"uris": batch}
            )
            response.raise_for_status()
    
    return True

async def get_playlist_tracks(access_token: str, playlist_id: str) -> List[Dict[str, Any]]:
    """
    Get all tracks from a playlist.
    
    Args:
        access_token: Valid Spotify access token
        playlist_id: Spotify playlist ID
        
    Returns:
        List of tracks in playlist
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    tracks = []
    offset = 0
    
    async with httpx.AsyncClient() as client:
        while True:
            params = {"offset": offset, "limit": 50}
            response = await client.get(
                f"{SPOTIFY_API_BASE}/playlists/{playlist_id}/tracks",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            for item in data.get("items", []):
                track = item.get("track")
                if track:
                    tracks.append({
                        "id": track["id"],
                        "name": track["name"],
                        "artists": [artist["name"] for artist in track.get("artists", [])],
                        "uri": track["uri"]
                    })
            
            offset += len(data.get("items", []))
            if not data.get("next"):
                break
    
    return tracks
