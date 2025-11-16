from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    id: str
    spotify_id: str
    display_name: str
    email: str
    followers: int
    profile_url: str
    image_url: Optional[str] = None
    plan_type: str

class UserStats(BaseModel):
    user_id: str
    top_tracks: List[dict]
    top_artists: List[dict]
    top_genres: List[str]
    listening_stats: dict

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str
    expires_in: int
    expires_at: float

class PlaylistCreate(BaseModel):
    name: str
    description: Optional[str] = None
    public: bool = False

class PlaylistUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    public: Optional[bool] = None

class BlendRequest(BaseModel):
    user_id1: str
    user_id2: str
    playlist_name: Optional[str] = None

class AIRequest(BaseModel):
    user_id: str
    prompt: str
    context: Optional[dict] = None
