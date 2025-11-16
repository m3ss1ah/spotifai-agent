import os
import hashlib
import secrets
import base64
import time
from typing import Dict, Tuple
from urllib.parse import urlencode
import httpx
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:3000/callback")

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

# Store state and PKCE codes for validation
_auth_states: Dict[str, dict] = {}

def generate_pkce() -> Tuple[str, str]:
    """
    Generate PKCE code_verifier and code_challenge.
    
    Returns:
        Tuple of (code_verifier, code_challenge)
    """
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8')
    code_verifier = code_verifier.replace('=', '')
    
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).decode('utf-8').replace('=', '')
    
    return code_verifier, code_challenge

def generate_auth_url() -> Tuple[str, str]:
    """
    Generate Spotify OAuth authorization URL with PKCE.
    
    Returns:
        Tuple of (auth_url, state)
    """
    state = secrets.token_urlsafe(32)
    code_verifier, code_challenge = generate_pkce()
    
    # Store state and PKCE for later validation
    _auth_states[state] = {
        "code_verifier": code_verifier,
        "timestamp": time.time()
    }
    
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "state": state,
        "scope": "user-read-private user-read-email user-top-read playlist-modify-public playlist-modify-private",
        "code_challenge_method": "S256",
        "code_challenge": code_challenge
    }
    
    auth_url = f"{SPOTIFY_AUTH_URL}?{urlencode(params)}"
    return auth_url, state

async def exchange_code_for_tokens(code: str, state: str) -> Dict[str, str]:
    """
    Exchange authorization code for access and refresh tokens.
    Validates state and uses PKCE for additional security.
    
    Args:
        code: Authorization code from Spotify redirect
        state: State parameter for CSRF protection
        
    Returns:
        Dictionary with access_token, refresh_token, and expires_in
    """
    # Validate state
    if state not in _auth_states:
        raise ValueError("Invalid state parameter")
    
    auth_data = _auth_states.pop(state)
    
    # Token request with PKCE
    data = {
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "code_verifier": auth_data["code_verifier"]
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(SPOTIFY_TOKEN_URL, data=data)
        response.raise_for_status()
        tokens = response.json()
    
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens.get("refresh_token"),
        "expires_in": tokens.get("expires_in", 3600),
        "expires_at": time.time() + tokens.get("expires_in", 3600)
    }

async def refresh_access_token(refresh_token: str) -> Dict[str, str]:
    """
    Refresh access token using refresh token.
    
    Args:
        refresh_token: Valid refresh token
        
    Returns:
        Dictionary with new access_token and expires_in
    """
    data = {
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(SPOTIFY_TOKEN_URL, data=data)
        response.raise_for_status()
        tokens = response.json()
    
    return {
        "access_token": tokens["access_token"],
        "expires_in": tokens.get("expires_in", 3600),
        "expires_at": time.time() + tokens.get("expires_in", 3600)
    }
