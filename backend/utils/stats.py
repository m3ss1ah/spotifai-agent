from typing import List, Dict, Any, Tuple

def extract_genres_from_artists(artists: List[Dict[str, Any]]) -> List[Tuple[str, int]]:
    """
    Extract and count genres from artists.
    
    Args:
        artists: List of artist dictionaries with genres
        
    Returns:
        List of (genre, count) tuples sorted by count
    """
    genre_count = {}
    
    for artist in artists:
        for genre in artist.get("genres", []):
            genre_count[genre] = genre_count.get(genre, 0) + 1
    
    return sorted(genre_count.items(), key=lambda x: x[1], reverse=True)

def calculate_similarity_score(user1_genres: List[str], user2_genres: List[str]) -> float:
    """
    Calculate similarity score between two users based on genres.
    
    Args:
        user1_genres: List of genres for user 1
        user2_genres: List of genres for user 2
        
    Returns:
        Similarity score between 0 and 1
    """
    if not user1_genres or not user2_genres:
        return 0.0
    
    set1 = set(user1_genres[:20])  # Use top 20 genres
    set2 = set(user2_genres[:20])
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0.0

def deduplicate_tracks(tracks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove duplicate tracks from list.
    
    Args:
        tracks: List of track dictionaries
        
    Returns:
        List of unique tracks (keeping first occurrence)
    """
    seen_ids = set()
    unique_tracks = []
    
    for track in tracks:
        track_id = track.get("id")
        if track_id not in seen_ids:
            seen_ids.add(track_id)
            unique_tracks.append(track)
    
    return unique_tracks

def merge_playlists(playlists: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """
    Merge multiple playlists into one, removing duplicates.
    
    Args:
        playlists: List of playlists (each is a list of tracks)
        
    Returns:
        Merged list of unique tracks
    """
    all_tracks = []
    for playlist in playlists:
        all_tracks.extend(playlist)
    
    return deduplicate_tracks(all_tracks)

def calculate_listening_stats(tracks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate listening statistics from tracks.
    
    Args:
        tracks: List of tracks with popularity
        
    Returns:
        Dictionary with statistics
    """
    if not tracks:
        return {
            "total_tracks": 0,
            "avg_popularity": 0,
            "max_popularity": 0,
            "min_popularity": 0
        }
    
    popularities = [t.get("popularity", 0) for t in tracks]
    
    return {
        "total_tracks": len(tracks),
        "avg_popularity": sum(popularities) / len(popularities),
        "max_popularity": max(popularities),
        "min_popularity": min(popularities)
    }
