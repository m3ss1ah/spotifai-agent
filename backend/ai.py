import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# LangChain imports
try:
    from langchain_ollama import OllamaLLM
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

class SpotifyAIAssistant:
    """
    AI Assistant for Spotify-related tasks using LLaMA via LangChain.
    """
    
    def __init__(self):
        self.model_name = OLLAMA_MODEL
        self.base_url = OLLAMA_BASE_URL
        
        if LANGCHAIN_AVAILABLE:
            self.llm = OllamaLLM(
                model=self.model_name,
                base_url=self.base_url,
                temperature=0.7
            )
        else:
            self.llm = None
    
    async def generate_playlist_name(self, genres: List[str], mood: Optional[str] = None) -> str:
        """
        Generate a creative playlist name using AI.
        
        Args:
            genres: List of genres
            mood: Optional mood descriptor
            
        Returns:
            Generated playlist name
        """
        if not self.llm:
            return self._fallback_playlist_name(genres, mood)
        
        genres_str = ", ".join(genres[:5])
        mood_str = f" with a {mood} vibe" if mood else ""
        
        prompt = f"""Generate a creative and catchy Spotify playlist name for a playlist with these genres: {genres_str}{mood_str}.
The name should be short (2-5 words), creative, and relevant to the genres.
Only respond with the playlist name, nothing else."""
        
        try:
            result = self.llm.invoke(prompt)
            return result.strip()
        except Exception:
            return self._fallback_playlist_name(genres, mood)
    
    async def analyze_mood(self, top_tracks: List[Dict[str, Any]], top_artists: List[Dict[str, Any]]) -> str:
        """
        Analyze user's listening mood based on top tracks and artists.
        
        Args:
            top_tracks: List of user's top tracks
            top_artists: List of user's top artists
            
        Returns:
            Mood analysis as string
        """
        if not self.llm:
            return self._fallback_mood_analysis(top_tracks, top_artists)
        
        track_names = ", ".join([t.get("name", "") for t in top_tracks[:5]])
        artist_names = ", ".join([a.get("name", "") for a in top_artists[:5]])
        genres = ", ".join(list(set([g for a in top_artists for g in a.get("genres", [])][:5])))
        
        prompt = f"""Analyze the following user's music taste and describe their listening mood in 2-3 sentences:
Top tracks: {track_names}
Top artists: {artist_names}
Genres: {genres}

Be creative and insightful about their mood and music preferences."""
        
        try:
            result = self.llm.invoke(prompt)
            return result.strip()
        except Exception:
            return self._fallback_mood_analysis(top_tracks, top_artists)
    
    async def fix_playlist(self, playlist_name: str, tracks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze and suggest improvements to a playlist.
        
        Args:
            playlist_name: Name of the playlist
            tracks: List of tracks in the playlist
            
        Returns:
            Dictionary with suggestions and recommendations
        """
        if not self.llm:
            return self._fallback_playlist_fix(playlist_name, tracks)
        
        track_count = len(tracks)
        track_names = ", ".join([t.get("name", "") for t in tracks[:10]])
        
        prompt = f"""I have a Spotify playlist called "{playlist_name}" with {track_count} tracks.
Some example tracks: {track_names}

Analyze this playlist and provide:
1. What the theme/mood of the playlist is
2. 2-3 suggestions to improve it
3. Whether the tracks flow well together

Keep response concise and actionable."""
        
        try:
            analysis = self.llm.invoke(prompt)
            return {
                "playlist": playlist_name,
                "track_count": track_count,
                "analysis": analysis.strip(),
                "suggestions": self._extract_suggestions(analysis)
            }
        except Exception:
            return self._fallback_playlist_fix(playlist_name, tracks)
    
    async def generate_taste_summary(self, top_tracks: List[Dict[str, Any]], 
                                     top_artists: List[Dict[str, Any]], 
                                     top_genres: List[str]) -> str:
        """
        Generate a summary of the user's music taste.
        
        Args:
            top_tracks: List of top tracks
            top_artists: List of top artists
            top_genres: List of top genres
            
        Returns:
            Taste summary as string
        """
        if not self.llm:
            return self._fallback_taste_summary(top_tracks, top_artists, top_genres)
        
        track_names = ", ".join([t.get("name", "") for t in top_tracks[:5]])
        artist_names = ", ".join([a.get("name", "") for a in top_artists[:5]])
        genres_str = ", ".join(top_genres[:5])
        
        prompt = f"""Write a fun and insightful 3-4 sentence summary of someone's music taste based on:
Top 5 tracks: {track_names}
Top 5 artists: {artist_names}
Top genres: {genres_str}

Make it personal and engaging, like you're describing their musical personality."""
        
        try:
            result = self.llm.invoke(prompt)
            return result.strip()
        except Exception:
            return self._fallback_taste_summary(top_tracks, top_artists, top_genres)
    
    def _fallback_playlist_name(self, genres: List[str], mood: Optional[str] = None) -> str:
        """Fallback playlist name generation."""
        adjectives = ["Ultimate", "Essential", "Perfect", "Best Of", "Vibes"]
        base = f"{adjectives[hash(str(genres)) % len(adjectives)]} {genres[0].title() if genres else 'Mixed'}"
        if mood:
            base += f" - {mood}"
        return base
    
    def _fallback_mood_analysis(self, top_tracks: List[Dict[str, Any]], 
                                top_artists: List[Dict[str, Any]]) -> str:
        """Fallback mood analysis."""
        return "Your taste spans across diverse genres with energetic and emotional tracks that suggest you enjoy both introspective and upbeat music."
    
    def _fallback_playlist_fix(self, playlist_name: str, tracks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback playlist analysis."""
        return {
            "playlist": playlist_name,
            "track_count": len(tracks),
            "analysis": f"Your playlist '{playlist_name}' has {len(tracks)} tracks with good variety.",
            "suggestions": ["Add more recent tracks", "Consider track flow and BPM", "Mix tempos for better listening experience"]
        }
    
    def _fallback_taste_summary(self, top_tracks: List[Dict[str, Any]], 
                               top_artists: List[Dict[str, Any]], 
                               top_genres: List[str]) -> str:
        """Fallback taste summary."""
        main_genre = top_genres[0] if top_genres else "diverse music"
        main_artist = top_artists[0].get("name", "multiple artists") if top_artists else "various artists"
        return f"You're a fan of {main_genre} with {main_artist} as a top artist. Your taste reflects a keen ear for quality production and meaningful lyrics."
    
    def _extract_suggestions(self, analysis: str) -> List[str]:
        """Extract suggestions from analysis text."""
        lines = analysis.split('\n')
        suggestions = [line.strip() for line in lines if line.strip() and any(
            keyword in line.lower() for keyword in ['suggest', 'try', 'add', 'consider', 'could']
        )]
        return suggestions[:3]
