"""
Unit tests for MusicBot: guardrail, index, scoring, retrieval, and confidence.
These tests run without the docs/ folder and without a Gemini API key.
"""

import pytest
from musicbot import MusicBot
from src.recommender import score_song, recommend_songs


# ---------------------------------------------------------------------------
# Fixture: MusicBot loaded with synthetic in-memory documents
# ---------------------------------------------------------------------------

def make_bot(docs=None):
    """Return a MusicBot with a custom document list, no real docs/ folder."""
    bot = MusicBot(docs_folder="__nonexistent__")
    if docs is not None:
        bot.documents = docs
        bot.index = bot.build_index(docs)
    return bot


FAKE_DOCS = [
    ("lofi.md",    "lofi songs are chill and acoustic. Focus Flow is a lofi track with low energy."),
    ("workout.md", "workout songs have high energy and intense mood. Iron Cathedral is metal and angry."),
    ("artists.md", "Neon Echo is a pop artist. LoRoom makes lofi music. Gravemass plays metal."),
]


# ---------------------------------------------------------------------------
# Guardrail tests
# ---------------------------------------------------------------------------

class TestGuardrail:
    def test_music_query_passes(self):
        bot = make_bot()
        assert bot.is_on_topic("What songs have the highest energy?") is True

    def test_off_topic_query_blocked(self):
        bot = make_bot()
        assert bot.is_on_topic("What is the capital of France?") is False

    def test_genre_keyword_passes(self):
        bot = make_bot()
        assert bot.is_on_topic("Show me all the jazz tracks") is True

    def test_mood_keyword_passes(self):
        bot = make_bot()
        assert bot.is_on_topic("I want something relaxed") is True

    def test_answer_retrieval_only_blocks_off_topic(self):
        bot = make_bot(FAKE_DOCS)
        result = bot.answer_retrieval_only("Who won the World Cup?")
        assert result == "I can only answer questions about the music catalog."


# ---------------------------------------------------------------------------
# Index and scoring tests
# ---------------------------------------------------------------------------

class TestIndexAndScoring:
    def test_build_index_maps_tokens_to_files(self):
        bot = make_bot(FAKE_DOCS)
        assert "lofi" in bot.index
        assert "lofi.md" in bot.index["lofi"]

    def test_build_index_no_duplicate_filenames(self):
        bot = make_bot(FAKE_DOCS)
        for filenames in bot.index.values():
            assert len(filenames) == len(set(filenames))

    def test_score_document_whole_word_match(self):
        bot = make_bot()
        # "in" should NOT match inside "intense" or "interesting"
        score = bot.score_document("in", "intense interesting instruments")
        assert score == 0

    def test_score_document_deduplicates_query_tokens(self):
        bot = make_bot()
        # Repeating "lofi" twice should count as 1 unique match, not 2
        score_repeated = bot.score_document("lofi lofi", "lofi music is chill")
        score_single   = bot.score_document("lofi",      "lofi music is chill")
        assert score_repeated == score_single == 1

    def test_score_document_counts_matched_tokens(self):
        bot = make_bot()
        score = bot.score_document("high energy intense", "high energy intense workout songs")
        assert score == 3


# ---------------------------------------------------------------------------
# Retrieval tests
# ---------------------------------------------------------------------------

class TestRetrieval:
    def test_retrieve_returns_relevant_snippet(self):
        bot = make_bot(FAKE_DOCS)
        snippets = bot.retrieve("lofi songs chill", top_k=1, min_score=1)
        assert len(snippets) == 1
        filename, text, score = snippets[0]
        assert filename == "lofi.md"

    def test_retrieve_returns_empty_for_no_match(self):
        bot = make_bot(FAKE_DOCS)
        snippets = bot.retrieve("classical piano baroque", top_k=3, min_score=2)
        assert snippets == []

    def test_retrieve_sorted_by_score_descending(self):
        bot = make_bot(FAKE_DOCS)
        snippets = bot.retrieve("lofi chill acoustic energy", top_k=3, min_score=1)
        scores = [s for _, _, s in snippets]
        assert scores == sorted(scores, reverse=True)

    def test_retrieval_confidence_zero_when_no_snippets(self):
        bot = make_bot(FAKE_DOCS)
        assert bot.retrieval_confidence("anything", []) == 0.0

    def test_retrieval_confidence_nonzero_on_match(self):
        bot = make_bot(FAKE_DOCS)
        snippets = bot.retrieve("lofi songs", top_k=1, min_score=1)
        confidence = bot.retrieval_confidence("lofi songs", snippets)
        assert 0.0 < confidence <= 1.0


# ---------------------------------------------------------------------------
# Recommender scoring tests
# ---------------------------------------------------------------------------

class TestRecommenderScoring:
    BASE_SONG = {
        "id": 1, "title": "Test", "artist": "A", "genre": "pop", "mood": "happy",
        "energy": 0.8, "valence": 0.9, "danceability": 0.8, "acousticness": 0.2,
        "instrumentalness": 0.0, "speechiness": 0.0, "liveness": 0.0, "tempo_bpm": 120,
    }

    def test_genre_match_adds_two_points(self):
        prefs = {"genre": "pop", "mood": "happy", "target_energy": 0.8, "likes_acoustic": False}
        song = {**self.BASE_SONG}
        score, reasons = score_song(prefs, song)
        genre_reason = [r for r in reasons if "genre match" in r]
        assert genre_reason, "Expected a genre match reason"
        assert score > 4.0  # genre(2) + energy close(~2) + acoustic(~0.4) > 4

    def test_genre_miss_adds_zero(self):
        prefs = {"genre": "metal", "mood": "angry", "target_energy": 0.8, "likes_acoustic": False}
        song = {**self.BASE_SONG}
        score, reasons = score_song(prefs, song)
        genre_reason = [r for r in reasons if "genre match" in r]
        assert not genre_reason

    def test_energy_penalty_increases_with_distance(self):
        prefs_close = {"genre": "x", "mood": "x", "target_energy": 0.8, "likes_acoustic": False}
        prefs_far   = {"genre": "x", "mood": "x", "target_energy": 0.1, "likes_acoustic": False}
        song = {**self.BASE_SONG}
        score_close, _ = score_song(prefs_close, song)
        score_far,   _ = score_song(prefs_far, song)
        assert score_close > score_far

    def test_recommend_songs_sorted_by_score(self):
        pop_song = {**self.BASE_SONG}
        lofi_song = {
            **self.BASE_SONG,
            "id": 2, "title": "Lofi Loop", "genre": "lofi", "mood": "chill",
            "energy": 0.4, "acousticness": 0.9,
        }
        prefs = {"genre": "pop", "mood": "happy", "target_energy": 0.8, "likes_acoustic": False}
        results = recommend_songs(prefs, [pop_song, lofi_song], k=2)
        top_song, top_score, _ = results[0]
        assert top_song["genre"] == "pop"
        assert top_score > results[1][1]
