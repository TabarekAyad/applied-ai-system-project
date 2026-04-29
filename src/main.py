"""
Command line runner for the Music Recommender Simulation and MusicBot.

Music Recommender: content-based scoring over a song catalog.
MusicBot: three-mode Q&A assistant (naive LLM, retrieval only, RAG).
"""

from src.recommender import load_songs, recommend_songs

# MusicBot imports — only available once musicbot.py, llm_client.py, dataset.py exist.
try:
    from dotenv import load_dotenv
    load_dotenv()
    from musicbot import MusicBot
    from llm_client import GeminiClient
    from dataset import SAMPLE_QUERIES
    _MUSICBOT_AVAILABLE = True
except ImportError:
    _MUSICBOT_AVAILABLE = False


ADVERSARIAL_PROFILES = [
    {
        # Energy 0.9 pulls toward rock/metal; sad mood pulls toward folk/lofi.
        # The two signals point in opposite directions — who wins?
        "name":           "EDGE: Conflicting Energy vs Mood",
        "genre":          "rock",
        "mood":           "sad",
        "target_energy":  0.90,
        "likes_acoustic": False,
    },
    {
        # Genre that exists in catalog with only one song (metal).
        # After Iron Cathedral, what fills positions 2-5?
        "name":           "EDGE: Single-Song Genre (metal)",
        "genre":          "metal",
        "mood":           "angry",
        "target_energy":  0.95,
        "likes_acoustic": False,
    },
    {
        # Energy 0.5 is equidistant from many songs — nearly every song
        # gets a similar energy score, so genre/mood dominate everything.
        "name":           "EDGE: Dead-Center Energy (0.5)",
        "genre":          "jazz",
        "mood":           "relaxed",
        "target_energy":  0.50,
        "likes_acoustic": True,
    },
    {
        # likes_acoustic=True but high energy target — high-energy songs
        # are almost always electronic (low acousticness). Can a song satisfy both?
        "name":           "EDGE: Acoustic + High Energy Contradiction",
        "genre":          "folk",
        "mood":           "intense",
        "target_energy":  0.90,
        "likes_acoustic": True,
    },
    {
        # Genre and mood that share zero songs in the catalog.
        # Pure energy + acoustic scoring drives all results.
        "name":           "EDGE: No Catalog Match (classical + angry)",
        "genre":          "classical",
        "mood":           "angry",
        "target_energy":  0.50,
        "likes_acoustic": False,
    },
]

PROFILES = [
    {
        "name":           "High-Energy Pop",
        "genre":          "pop",
        "mood":           "happy",
        "target_energy":  0.85,
        "likes_acoustic": False,
    },
    {
        "name":           "Chill Lofi",
        "genre":          "lofi",
        "mood":           "focused",
        "target_energy":  0.40,
        "likes_acoustic": True,
    },
    {
        "name":           "Deep Intense Rock",
        "genre":          "rock",
        "mood":           "intense",
        "target_energy":  0.90,
        "likes_acoustic": False,
    },
    {
        "name":           "Melancholic Evening",
        "genre":          "folk",
        "mood":           "sad",
        "target_energy":  0.30,
        "likes_acoustic": True,
    },
    {
        "name":           "Friday Night EDM",
        "genre":          "edm",
        "mood":           "intense",
        "target_energy":  0.92,
        "likes_acoustic": False,
    },
]


def print_recommendations(profile: dict, songs: list, k: int = 5) -> None:
    """Print a formatted recommendation block for one user profile."""
    print(f"\n{'='*54}")
    print(f"  Profile : {profile['name']}")
    print(f"{'='*54}")
    print(f"  Genre   : {profile['genre']}")
    print(f"  Mood    : {profile['mood']}")
    print(f"  Energy  : {profile['target_energy']}")
    print(f"  Acoustic: {'yes' if profile['likes_acoustic'] else 'no'}")

    user_prefs = {k: v for k, v in profile.items() if k != "name"}
    recommendations = recommend_songs(user_prefs, songs, k=k)

    print(f"\n  Top {len(recommendations)} Recommendations:\n")
    for i, (song, score, reasons) in enumerate(recommendations, 1):
        filled = round(score / 6.0 * 20)
        bar = f"[{'#' * filled}{'-' * (20 - filled)}]"
        print(f"  #{i}  {song['title']} by {song['artist']}")
        print(f"       Score : {score:.3f} / 6.0  {bar}")
        print(f"       Why   :")
        for reason in reasons:
            print(f"                - {reason}")
        print()


def run_recommender() -> None:
    """Run the music recommender over all standard and adversarial profiles."""
    songs = load_songs("data/songs.csv")
    print(f"\n{'='*54}")
    print(f"  Catalog: {len(songs)} songs loaded")
    print(f"{'='*54}")
    for song in songs:
        print(f"  {song['id']:>2}. {song['title']:<28} [{song['genre']:<10}] [{song['mood']:<10}] energy={song['energy']:.2f}")

    for profile in PROFILES:
        print_recommendations(profile, songs, k=5)

    print(f"\n{'='*54}")
    print(f"  ADVERSARIAL / EDGE CASE PROFILES")
    print(f"{'='*54}")
    for profile in ADVERSARIAL_PROFILES:
        print_recommendations(profile, songs, k=5)


# ── MusicBot ──────────────────────────────────────────────────────────────────

def _try_create_llm_client():
    """Return (GeminiClient, True) or (None, False) if the key is missing."""
    try:
        client = GeminiClient()
        return client, True
    except RuntimeError as exc:
        print("Warning: LLM features are disabled.")
        print(f"Reason: {exc}")
        print("You can still run retrieval only mode.\n")
        return None, False


def _choose_musicbot_mode(has_llm: bool) -> str:
    """Print the mode menu and return the user's choice."""
    print("\nChoose a mode:")
    if has_llm:
        print("  1) Naive LLM over full docs (no retrieval)")
    else:
        print("  1) Naive LLM over full docs (unavailable — no GEMINI_API_KEY)")
    print("  2) Retrieval only (no LLM)")
    if has_llm:
        print("  3) RAG (retrieval + LLM)")
    else:
        print("  3) RAG (unavailable — no GEMINI_API_KEY)")
    print("  q) Quit MusicBot")
    return input("Enter choice: ").strip().lower()


def _get_query_or_samples():
    """Return (list of query strings, label). Uses SAMPLE_QUERIES if input is blank."""
    print("\nPress Enter to run built-in sample queries.")
    custom = input("Or type a single custom query: ").strip()
    if custom:
        return [custom], "custom query"
    return SAMPLE_QUERIES, "sample queries"


def _run_naive_llm(musicbot, has_llm: bool) -> None:
    """Mode 1: send full corpus to LLM and generate an answer."""
    if not has_llm or musicbot.llm_client is None:
        print("\nNaive LLM mode is not available (no GEMINI_API_KEY).\n")
        return
    queries, label = _get_query_or_samples()
    print(f"\nRunning naive LLM mode on {label}...\n")
    all_text = musicbot.full_corpus_text()
    for query in queries:
        print("=" * 60)
        print(f"Question: {query}\n")
        print("Answer:")
        print(musicbot.llm_client.naive_answer_over_full_docs(query, all_text))
        print()


def _run_retrieval_only(musicbot) -> None:
    """Mode 2: retrieve and rank snippets; no LLM."""
    queries, label = _get_query_or_samples()
    print(f"\nRunning retrieval only mode on {label}...\n")
    for query in queries:
        print("=" * 60)
        print(f"Question: {query}\n")
        print("Retrieved snippets:")
        print(musicbot.answer_retrieval_only(query))
        print()


def _run_rag(musicbot, has_llm: bool) -> None:
    """Mode 3: retrieve snippets then generate a grounded LLM answer."""
    if not has_llm or musicbot.llm_client is None:
        print("\nRAG mode is not available (no GEMINI_API_KEY).\n")
        return
    queries, label = _get_query_or_samples()
    print(f"\nRunning RAG mode on {label}...\n")
    for query in queries:
        print("=" * 60)
        print(f"Question: {query}\n")
        print("Answer:")
        print(musicbot.answer_rag(query))
        print()


def run_musicbot() -> None:
    """Interactive loop for the three MusicBot modes."""
    if not _MUSICBOT_AVAILABLE:
        print("\nMusicBot is not available yet.")
        print("Required modules (musicbot.py, llm_client.py, dataset.py) are missing.\n")
        return

    print("\nMusicBot")
    print("========\n")
    llm_client, has_llm = _try_create_llm_client()
    musicbot = MusicBot(llm_client=llm_client)

    while True:
        choice = _choose_musicbot_mode(has_llm)
        if choice == "q":
            print("\nExiting MusicBot.\n")
            break
        elif choice == "1":
            _run_naive_llm(musicbot, has_llm)
        elif choice == "2":
            _run_retrieval_only(musicbot)
        elif choice == "3":
            _run_rag(musicbot, has_llm)
        else:
            print("\nUnknown choice. Please pick 1, 2, 3, or q.\n")


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    """Top-level menu: choose between the music recommender and MusicBot."""
    print("\n╔══════════════════════════════════════╗")
    print("║   Applied AI System — Main Menu      ║")
    print("╚══════════════════════════════════════╝")
    print("  1) Music Recommender")
    print("  2) MusicBot (Q&A assistant)")
    print("  q) Quit")
    choice = input("\nEnter choice: ").strip().lower()

    if choice == "1":
        run_recommender()
    elif choice == "2":
        run_musicbot()
    elif choice == "q":
        print("Goodbye.")
    else:
        print("Unknown choice.")


if __name__ == "__main__":
    main()
