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

**21 out of 21 automated tests passed.** Confidence scores averaged 0.67–1.0 across the 9 sample queries; all fell to 0.0 for off-topic queries, correctly triggering the guardrail before any retrieval ran.

### Automated tests (`pytest`)

Two test files cover both subsystems:

| File | Tests | What is covered |
|---|---|---|
| `tests/test_musicbot.py` | 19 | Guardrail (on-topic/off-topic), index structure, `score_document` whole-word matching, token deduplication, retrieval ranking, confidence scoring, recommender scoring formula |
| `tests/test_recommender.py` | 2 | `Recommender.recommend` returns results sorted by genre/mood match; `explain_recommendation` returns a non-empty string |

### Confidence scoring

`MusicBot.retrieval_confidence()` returns a 0.0–1.0 score after each retrieval. It is computed as `top_snippet_score / num_unique_query_tokens`, capped at 1.0. It appears in the retrieval-only output header and is logged for every RAG call. Confidence stays at 0.0 whenever no snippets pass the minimum threshold, which also means the guardrail or the "I do not know" fallback fires — so confidence directly predicts when the system will decline to answer.

### Logging and error handling

- `musicbot.py` logs: doc loading count, index token count, guardrail trigger (mode + query), retrieved snippet count, and confidence per call
- `llm_client.py` logs: client initialization, each API call (query + corpus size or snippet count), response size, and exceptions before re-raising
- Missing `docs/` folder logs a warning and returns an empty document list instead of crashing
- Unreadable individual files log an error and are skipped; the rest of the corpus still loads

### Human evaluation

All 9 sample queries were run manually in each of the 3 MusicBot modes. Retrieval-only and RAG returned relevant, factually correct answers for 8 of 9 queries. The one partial failure: "Which artists appear in the catalog?" retrieved the correct `artists.md` chunk but the RAG answer omitted 2 of 18 artists because the relevant text was split across two chunks and only the top-1 chunk was sent to the model. Increasing `top_k` from 1 to 3 resolved this.

5 adversarial recommender profiles were also evaluated manually. All 5 produced the expected top result and showed the predicted scoring behavior documented in the edge case table below.

### What failed and how it was fixed

| Bug | Root Cause | Fix |
|---|---|---|
| RAG returned "I do not know" for all queries | `score_document` counted duplicate tokens and matched substrings ("in" inside "intense"), surfacing wrong documents | Deduplicate query tokens; use `\b\w+\b` whole-word matching |
| RAG still failed after above fix | Threshold check was `score > effective_min` (strict greater), blocking chunks that exactly met the threshold | Changed to `score >= effective_min` |
| Naive mode ignored the corpus | `naive_answer_over_full_docs` did not include `all_text` in the prompt | Fixed prompt template to embed the full corpus |
| `load_fallback_documents()` crashed | Called `.items()` on a list | Converted `FALLBACK_DOCS` to `(topic, text)` tuples and used `list()` |
| Deprecation errors on startup | `google.generativeai` removed; code used old `genai.configure()` API | Migrated to `google.genai` with `genai.Client()` and `client.models.generate_content()` |
| No guardrail on Naive mode | `answer_naive` called LLM without a topic check | Added `is_on_topic()` check at the top of `answer_naive` |
| Starter tests crashing | `Song` dataclass gained 3 fields; test fixtures missing them | Added `instrumentalness`, `speechiness`, `liveness` to both test Song instances |

### What to test next

- Synonym coverage: "high tempo" vs "energetic" — inverted index cannot bridge these
- Adversarial guardrail bypass via music-adjacent phrasing (e.g., "what country has the most pop music?")
- Multi-turn consistency: does the same query return the same snippets on repeated runs?

---

## Reflection and Ethics

### What are the limitations or biases in your system?

**Music Recommender**

The scoring formula contains several embedded assumptions that act as biases:

- **Genre is binary.** A genre mismatch always scores 0.0 regardless of cultural proximity. Rock and pop are sonically adjacent; rock and classical are not. The system treats both misses identically, so a user who likes indie pop may receive EDM before folk because the energy number happened to align.
- **Single-mood profile.** A user who listens to `chill` music when studying and `intense` music when exercising cannot be represented. Forcing one mood means context-switching listeners always get a compromised result, and the system silently chooses for them.
- **Small catalog overfit.** With only 20 songs, genres like `metal`, `classical`, and `edm` have exactly one representative each. A user whose favorite genre is `metal` will always receive *Iron Cathedral* as their top result regardless of how poorly the energy or mood matches, because there are no alternatives.
- **Energy dominates when categorical signals fail.** A song with a perfect energy match but mismatched genre and mood can outrank a genre+mood match that sits at a slightly different energy level. This mirrors how real systems can recommend things that feel technically close but contextually wrong.
- **Acousticness is a boolean.** `likes_acoustic=True` rewards a song with acousticness 0.60 and one with 0.97 equally. This bluntness over-rewards sparse, near-silent tracks for users who might just want a "warmer" sound, not an unplugged performance.

**MusicBot**

- **Keyword-only guardrail.** The off-topic filter uses exact keyword matching. Queries phrased without any music vocabulary pass through unchecked (e.g., "What is energy?" has no music keyword but is ambiguous). Conversely, a genuinely off-topic question that happens to contain the word "pop" or "top" will pass the guardrail and reach the retrieval step.
- **Inverted index cannot handle synonyms.** A user asking "upbeat songs" will not match a document that only uses the word "energetic." The retrieval step has no semantic understanding — it only counts exact token overlap.
- **RAG answers are only as good as the retrieved chunks.** If the most relevant information is split across two chunks and only one is retrieved, the LLM's answer will be incomplete. The system has no way to signal that its answer is partial rather than complete.
- **LLM hallucination risk in Naive mode.** In mode 1, the full corpus is sent to Gemini with no constraints on what it can say beyond the prompt instructions. The model may still generate plausible-sounding but incorrect details about songs or artists not in the catalog.
- **Western and English-language catalog bias.** All 20 songs use English titles and Western genre labels. A user who primarily listens to K-pop, Afrobeats, or Bollywood would find no matching genre or mood labels, and the system would fall back entirely to energy and acousticness scoring — which are genre-agnostic but culturally blind.

---

### Could your AI be misused, and how would you prevent that?

**Realistic misuse scenarios**

| Scenario | Risk |
|---|---|
| Prompt injection via the query field | A crafted query could try to override the LLM's system prompt in RAG or Naive mode (e.g., "Ignore previous instructions and...") |
| Guardrail bypass through music-adjacent phrasing | Embedding a harmful request inside a music question ("What songs pair well with [harmful content]?") could slip past keyword filtering |
| API key exposure | If `.env` is accidentally committed to a public repository, the Gemini API key becomes publicly accessible |
| Scraping at scale | The system calls a paid API per query; an automated loop could generate large costs for the key owner |

**Mitigations already in place**

- The off-topic guardrail blocks the most obvious off-topic abuse before any LLM call is made, reducing unnecessary API usage.
- The RAG prompt explicitly instructs the model to answer only from retrieved snippets and refuse to invent information, which limits (but does not eliminate) prompt injection risk.
- `.env` is excluded from git via `.gitignore`, and `.env.example` contains only a placeholder, never a real key.
- Logging records every query and every LLM call, so unusual usage patterns are detectable after the fact.

**What would be needed for a production system**

A classroom project can accept these limitations, but a deployed system would require:
- **Input sanitization and length limits** on the query field to prevent injection attacks
- **Rate limiting** on API calls per session to prevent cost abuse
- **Prompt hardening** — moving the system instruction out of the user-visible prompt and into a separate system role, where it is harder to override
- **Semantic guardrail** — replacing or supplementing keyword matching with a classifier that detects intent, not just vocabulary
- **Output filtering** — a second pass over the LLM's response to catch cases where it generated content outside its allowed scope

Building this system made clear that safety is not a feature you add at the end — the guardrail, the logging, and the retrieval grounding all had to be designed into the architecture from the start, or the LLM would simply fill the gaps with uncontrolled output.

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
