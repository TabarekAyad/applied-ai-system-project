from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    instrumentalness: float
    speechiness: float
    liveness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

MOOD_NEIGHBORS = {
    "happy":     ["relaxed"],
    "chill":     ["relaxed", "focused"],
    "intense":   ["moody"],
    "moody":     ["intense"],
    "relaxed":   ["happy", "chill"],
    "focused":   ["chill"],
    "sad":       ["moody"],
    "dreamy":    ["chill", "relaxed"],
    "nostalgic": ["sad", "moody"],
    "romantic":  ["relaxed", "happy"],
    "angry":     ["intense"],
}

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against a user preference dict.
    Returns (total_score, reasons) where reasons explains each contribution.
    Max possible score: 6.0
    """
    score = 0.0
    reasons = []

    # Genre match: +2.0 exact, +0.0 miss
    if song["genre"] == user_prefs["genre"]:
        score += 2.0
        reasons.append(f"genre match ({song['genre']}) (+2.0)")

    # Mood match: +1.5 exact, +0.75 adjacent, +0.0 miss
    if song["mood"] == user_prefs["mood"]:
        score += 1.5
        reasons.append(f"mood match ({song['mood']}) (+1.5)")
    elif song["mood"] in MOOD_NEIGHBORS.get(user_prefs["mood"], []):
        score += 0.75
        reasons.append(f"adjacent mood ({song['mood']} ~ {user_prefs['mood']}) (+0.75)")

    # Energy similarity: up to +2.0 using squared distance penalty
    energy_pts = 2.0 * (1.0 - (song["energy"] - user_prefs["target_energy"]) ** 2)
    score += energy_pts
    reasons.append(f"energy {song['energy']} vs target {user_prefs['target_energy']} (+{energy_pts:.2f})")

    # Acoustic alignment: up to +0.5
    if user_prefs["likes_acoustic"]:
        acoustic_pts = 0.5 * song["acousticness"]
    else:
        acoustic_pts = 0.5 * (1.0 - song["acousticness"])
    score += acoustic_pts
    reasons.append(f"acoustic alignment (+{acoustic_pts:.2f})")

    return round(score, 3), reasons


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv

    int_fields   = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness",
                    "instrumentalness", "speechiness", "liveness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)

    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))

    scored.sort(key=lambda x: (x[1], x[0]["valence"]), reverse=True)

    return [(song, score, reasons) for song, score, reasons in scored[:k]]
