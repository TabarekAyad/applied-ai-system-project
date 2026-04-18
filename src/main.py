"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("../data/songs.csv")
    print(f"Loaded {len(songs)} songs:")
    for song in songs:
        print(f"  {song['id']:>2}. {song['title']} — {song['artist']} ({song['genre']}, {song['mood']}, energy={song['energy']})")

    # User taste profiles — swap the active one to test different recommendations

    # Profile 1: High-energy pop fan who wants upbeat workout music
    user_prefs = {
        "genre":          "pop",
        "mood":           "happy",
        "target_energy":  0.85,
        "likes_acoustic": False,
    }

    # Profile 2: Late-night focus session — lo-fi, calm, instrumental
    # user_prefs = {
    #     "genre":          "lofi",
    #     "mood":           "focused",
    #     "target_energy":  0.40,
    #     "likes_acoustic": True,
    # }

    # Profile 3: Melancholic evening — folk/indie, sad, acoustic storytelling
    # user_prefs = {
    #     "genre":          "folk",
    #     "mood":           "sad",
    #     "target_energy":  0.30,
    #     "likes_acoustic": True,
    # }

    # Profile 4: Friday night out — EDM/electronic, intense, high danceability
    # user_prefs = {
    #     "genre":          "edm",
    #     "mood":           "intense",
    #     "target_energy":  0.92,
    #     "likes_acoustic": False,
    # }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for i, (song, score, reasons) in enumerate(recommendations, 1):
        print(f"#{i} {song['title']} by {song['artist']}")
        print(f"    Score: {score:.3f} / 6.0")
        print(f"    Because:")
        for reason in reasons:
            print(f"      - {reason}")
        print()


if __name__ == "__main__":
    main()
