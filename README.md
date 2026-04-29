# MoodTune — Applied AI System

## Original Project

This project extends **Music Recommender System** (Modules 1–3), a content-based music recommendation engine. The original system scored a 20-song catalog against a user's taste profile (genre, mood, target energy, acoustic preference) using a weighted formula with a maximum score of 6.0. It returned the top 5 ranked songs with plain-language explanations for why each was recommended.

---

## Title and Summary

**MoodTune** is an applied AI system that combines a content-based music recommender with a Retrieval-Augmented Generation (RAG) Q&A assistant called MusicBot. The recommender scores songs against a user's taste profile and ranks them. MusicBot lets users ask natural-language questions about the catalog and answers them in three modes: naive LLM generation, keyword retrieval only, and full RAG (retrieval + LLM). Together, they demonstrate two distinct AI paradigms — rule-based scoring and language model reasoning — in a single runnable application.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     src/main.py                         │
│           Top-level menu: Recommender | MusicBot        │
└────────────────┬──────────────────┬─────────────────────┘
                 │                  │
     ┌───────────▼──────┐  ┌────────▼──────────────────┐
     │  Music Recommender│  │         MusicBot           │
     │  src/recommender.py│  │       musicbot.py          │
     │                  │  │                            │
     │  data/songs.csv  │  │  docs/*.md  ← knowledge    │
     │  20 songs        │  │  base (6 files)            │
     │                  │  │                            │
     │  Scoring formula │  │  ┌─────────────────────┐  │
     │  genre  0.20     │  │  │   Inverted Index     │  │
     │  mood   0.30     │  │  │   build_index()      │  │
     │  energy 0.40     │  │  │   retrieve()         │  │
     │  acoustic 0.10   │  │  └──────────┬──────────┘  │
     └──────────────────┘  │             │              │
                           │  ┌──────────▼──────────┐  │
                           │  │   llm_client.py      │  │
                           │  │   GeminiClient       │  │
                           │  │   gemini-2.5-flash   │  │
                           │  └─────────────────────┘  │
                           └───────────────────────────┘
```

**Music Recommender flow:**
1. Load `data/songs.csv` into a list of song dictionaries
2. User selects a taste profile (genre, mood, energy, acoustic preference)
3. Score every song with the weighted formula (max 6.0)
4. Return top 5 with a score bar and plain-language reasons

**MusicBot flow:**
1. Load and chunk all `.md` files in `docs/` into `(filename, text)` pairs
2. Build an inverted index mapping tokens → filenames
3. On each query, check the off-topic guardrail first
4. **Mode 1 — Naive:** send the full corpus text to Gemini with no filtering
5. **Mode 2 — Retrieval only:** score chunks against the query, return top 3 raw snippets
6. **Mode 3 — RAG:** retrieve top 3 snippets, then ask Gemini to answer using only those

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd applied-ai-system-project
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Mac / Linux
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your Gemini API key

MusicBot modes 1 (Naive) and 3 (RAG) call the Gemini API. The Music Recommender and MusicBot mode 2 (Retrieval only) work without a key.

- Get a free key at https://aistudio.google.com/app/apikeys
- Copy the example env file:

```bash
cp .env.example .env          # Mac / Linux
copy .env.example .env        # Windows
```

Open `.env` and replace the placeholder:

```
GEMINI_API_KEY=AIza...your_real_key_here
```

### 5. Run the application

```bash
python -m src.main
```

### 6. Run the tests

```bash
pytest
```

---

## Sample Interactions

### Example 1 — Music Recommender (Profile: Chill Lofi)

```
Enter profile number: 2

======================================================
  Profile : Chill Lofi
======================================================
  Genre   : lofi
  Mood    : focused
  Energy  : 0.4
  Acoustic: yes

  Top 5 Recommendations:

  #1  Focus Flow by LoRoom
       Score : 5.950 / 6.0  [####################]
       Why   :
                - Genre match: lofi
                - Mood match: focused
                - Energy close to target (0.40 vs 0.40)
                - Acoustic preference matched

  #2  Library Rain by Paper Lanterns
       Score : 5.008 / 6.0  [################----]
       Why   :
                - Genre match: lofi
                - Adjacent mood (chill ≈ focused)
                - Energy close to target (0.35 vs 0.40)
                - Acoustic preference matched
```

---

### Example 2 — MusicBot Mode 2 (Retrieval Only)

```
Question: What songs are available in the lofi genre?

Retrieved snippets:

[lofi_genre.md]
Songs in the lofi genre:
- Midnight Coding by LoRoom      | Mood: chill   | Energy: 0.42 | Acousticness: 0.71
- Library Rain by Paper Lanterns | Mood: chill   | Energy: 0.35 | Acousticness: 0.86
- Focus Flow by LoRoom           | Mood: focused | Energy: 0.40 | Acousticness: 0.78
All three lofi songs have low energy (0.35–0.42) and high acousticness...
```

---

### Example 3 — MusicBot Mode 3 (RAG)

```
Question: What song would you recommend for an intense workout?

Answer:
Based on the workout topic, the best songs for an intense workout are:

1. Iron Cathedral by Gravemass — energy 0.96 (metal/angry) — maximum intensity
2. Pulse Grid by Synthex — energy 0.94 (edm/intense) — driving electronic beat, great for cardio
3. Gym Hero by Max Pulse — energy 0.93 (pop/intense) — upbeat and motivating
4. Storm Runner by Voltline — energy 0.91 (rock/intense) — aggressive rock energy

These four songs have the highest energy scores in the catalog and are tagged
with intense or angry moods, making them ideal for high-intensity activities.
```

---

### Example 4 — MusicBot Off-Topic Guardrail

```
Question: What is the capital of France?

Answer:
I can only answer questions about the music catalog.
```

---

## Design Decisions

### Why content-based filtering for the recommender?

Content-based filtering scores songs against stated preferences rather than inferring taste from other users. This makes every recommendation fully explainable — you can always trace why a song appeared. The trade-off is that it cannot discover music outside the user's stated preferences the way collaborative filtering can.

### Why a fixed weighted formula?

The weights (energy 0.40, mood 0.30, genre 0.20, acoustic 0.10) reflect how strongly each feature affects the overall listening experience. A large energy mismatch ruins a session regardless of genre or mood, so energy carries the most weight. Mood captures why you're listening right now (context), while genre captures longer-term texture — hence mood outweighs genre. The trade-off is that these weights are manually tuned and not learned from data.

### Why an inverted index instead of embeddings for retrieval?

An inverted index is transparent, fast, and requires no external model. For a 6-file knowledge base, it retrieves the right documents reliably. The trade-off is that it cannot handle synonyms or semantic similarity — "high tempo" will not match a document that only uses the word "energetic." Embedding-based retrieval would handle this but adds cost and complexity.

### Why three separate modes in MusicBot?

The three modes exist to compare retrieval and generation strategies directly:
- **Naive LLM** shows what a model can do with all information but no structure — useful as a baseline but expensive and uncontrolled
- **Retrieval only** shows what keyword search alone returns — fully auditable, zero LLM cost, but outputs raw text the user must parse
- **RAG** combines both — the LLM generates a natural answer, but only from evidence the retrieval step selected — better grounding than naive, better readability than retrieval only

### Why an off-topic guardrail?

LLMs answer any question given to them. Without a guardrail, a user asking about world geography would get a confident, fabricated response in a music assistant. The keyword intersection check costs nothing and blocks clearly off-topic queries before any retrieval or API call runs.

---

## Testing Summary

### What worked well

- The content-based scoring formula produced sensible rankings across all 10 test profiles, including 5 adversarial edge cases designed to expose conflicts (e.g., high energy + sad mood, acoustic + high energy, genre with only one catalog entry)
- The off-topic guardrail correctly blocked every non-music query tested without false-positiving on music questions that used indirect phrasing
- RAG mode answered all 9 sample queries correctly after retrieval quality was fixed
- Graceful degradation worked as intended: when no API key is present, the app starts, disables modes 1 and 3, and lets the user run retrieval-only mode without crashing

### What failed and how it was fixed

| Bug | Root Cause | Fix |
|---|---|---|
| RAG returned "I do not know" for all queries | `score_document` counted duplicate tokens and matched substrings ("in" inside "intense"), causing wrong documents to rank first | Deduplicate query tokens; use `\b\w+\b` whole-word matching |
| RAG still failed after fix | Threshold check was `score > effective_min` (strict), blocking chunks with score exactly equal to the threshold | Changed to `score >= effective_min` |
| Naive mode ignored the corpus | `naive_answer_over_full_docs` did not include `all_text` in the prompt | Fixed the prompt template to embed the full corpus |
| `load_fallback_documents()` crashed | Called `.items()` on a list instead of a dict | Converted `FALLBACK_DOCS` to `(topic, text)` tuples and returned `list(FALLBACK_DOCS)` |
| Deprecation errors on startup | `google.generativeai` package removed; code used old `genai.configure()` API | Migrated to `google.genai` with `genai.Client(api_key=...)` and `client.models.generate_content()` |
| No guardrail on Naive mode | `answer_naive` called LLM directly without topic check | Added `is_on_topic()` check at the top of `answer_naive` |

### What I would test next

- Edge queries with synonyms ("high tempo" vs "energetic") to measure retrieval recall gaps
- Multi-turn conversation: does the system maintain context across questions?
- Adversarial prompts designed to jailbreak the off-topic guardrail via music-adjacent phrasing

---

## Reflection



---

## Project Structure

```
applied-ai-system-project/
├── src/
│   ├── main.py          # Entry point and CLI menus
│   └── recommender.py   # Scoring formula and catalog loader
├── data/
│   └── songs.csv        # 20-song catalog
├── docs/                # MusicBot knowledge base (6 .md files)
│   ├── catalog.md
│   ├── high_energy_songs.md
│   ├── genres_and_moods.md
│   ├── artists.md
│   ├── acoustic_songs.md
│   └── recommendations.md
├── musicbot.py          # MusicBot class: loading, indexing, retrieval, answering
├── llm_client.py        # GeminiClient wrapper (naive + RAG generation)
├── dataset.py           # Sample queries and fallback corpus
├── requirements.txt
├── .env.example         # API key template
└── README.md
```
