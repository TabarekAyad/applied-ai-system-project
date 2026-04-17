# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This project builds a simplified content-based music recommender that scores songs against a user taste profile and returns the best matches. Each song is described by numerical features (energy, valence, danceability, acousticness, tempo) and categorical labels (genre, mood). A user profile stores their preferences, and the recommender computes a weighted score for every song in the catalog — rewarding songs that are close to the user's target energy, match their mood, align with their genre, and fit their acoustic preference. The top-scoring songs are returned as recommendations with a plain-language explanation for each.

---

## How The System Works

Real-world recommendation systems like Spotify or YouTube don't just match songs to a static profile — they continuously learn from behavior (skips, replays, saves) and layer multiple signals together: what you've listened to, what similar users love, the audio properties of the song itself, and even the time of day you're listening. They operate at massive scale using techniques like matrix factorization, deep neural networks on raw audio, and reinforcement learning to optimize for long-term satisfaction rather than just the next click. This version prioritizes a simpler but principled approach: **content-based filtering using four song features — energy, mood, genre, and acousticness — weighted by how much each one reflects real listening intent.** Rather than guessing from other users' behavior, it scores each song directly against a user's stated preferences and ranks the results. The goal is a system that produces explainable, sensible recommendations — one where you can trace exactly why a song was suggested and verify that the logic matches how musical "vibe" actually works.

Explain your design in plain language.

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo

  Each song carries five numerical features and two categorical labels:
  - `energy` (0.0–1.0) — intensity and loudness; the primary scoring signal
  - `valence` (0.0–1.0) — musical positivity; used as a tie-breaker in ranking
  - `danceability` (0.0–1.0) — rhythmic regularity; available but passive in v1
  - `acousticness` (0.0–1.0) — absence of electronic production; scored against user preference
  - `tempo_bpm` (BPM) — speed of the beat; correlated with energy, passive in v1
  - `genre` (string) — categorical label matched against the user's favorite genre
  - `mood` (string) — categorical label matched against the user's favorite mood, with partial credit for adjacent moods

- What information does your `UserProfile` store

  ```
  favorite_genre   → string   e.g. "pop"
  favorite_mood    → string   e.g. "happy"
  target_energy    → float    e.g. 0.8
  likes_acoustic   → bool     e.g. False
  ```

- How does your `Recommender` compute a score for each song

  Each song receives a score between 0.0 and 1.0 from four weighted components:
  ```
  score = energy_score   × 0.40   ← squared distance from target_energy
        + mood_score     × 0.30   ← exact=1.0, adjacent mood=0.5, miss=0.0
        + genre_score    × 0.20   ← exact=1.0, miss=0.0
        + acoustic_score × 0.10   ← aligned with likes_acoustic boolean
  ```
  Energy carries the most weight because a large energy mismatch ruins a listening session regardless of other matches. Mood outweighs genre because it captures *why* you're listening right now (context), while genre captures longer-term taste (texture).

- How do you choose which songs to recommend

  1. Score every song in the catalog using the formula above
  2. Sort all songs by score, highest first
  3. Break ties using `valence` (happier-sounding songs win)
  4. Return the top `k` results (default `k=5`) with a plain-language explanation for each

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

