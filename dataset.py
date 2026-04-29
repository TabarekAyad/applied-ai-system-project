"""
Sample queries and fallback documentation corpus for MusicBot.

SAMPLE_QUERIES: realistic questions a user might ask about the catalog.
DOCS_CORPUS: text snippets MusicBot indexes and searches to answer questions.
"""

SAMPLE_QUERIES = [
    # Catalog exploration
    "Which songs have the highest energy in the catalog?",
    "Which songs have the lowest energy in the catalog?",
    "What songs are available in the lofi genre?",
    "What pop songs are in the catalog?",
    "Which songs are in the r&b genre?",
    "Are there any metal songs in the catalog?",
    "Which songs are electronic or EDM?",
    "What folk or indie folk songs are available?",
    "Which songs have a happy mood?",
    "Which songs have a sad mood?",
    "Which songs have a dreamy mood?",
    "Which songs have a relaxed mood?",
    "Which songs have a moody mood?",
    "List all acoustic songs in the catalog.",
    "Which songs are the least acoustic?",
    "Which songs are best for dancing?",
    "Which songs have the highest tempo?",
    "Which artists appear in the catalog?",
    "Which artists have more than one song in the catalog?",

    # Individual song lookup
    "Tell me about Sunrise City.",
    "What genre and mood is Night Drive Loop?",
    "How energetic is Iron Cathedral?",
    "Is Moonlit Sonata acoustic?",
    "What is the mood of Gold Chain Daydream?",
    "Who performs Coffee Shop Stories?",
    "Compare Focus Flow and Midnight Coding.",
    "Compare Cabin Smoke and Broken Compass.",

    # Recommendation reasoning
    "What song would you recommend for an intense workout?",
    "What would you suggest for a late-night study session?",
    "Which songs are best for someone who likes chill, acoustic music?",
    "What are the top songs for a high-energy pop lover?",
    "What should I play for a calm coffee shop vibe?",
    "What should I play for a sad acoustic evening?",
    "What songs would fit a dreamy nighttime playlist?",
    "What songs would fit a nostalgic drive?",
    "What should I play for a romantic relaxed mood?",
    "What would you suggest for a high-energy dance playlist?",
    "What should I play if I want angry or intense music?",
    "What songs are good for coding or focus?",
    "What would you recommend for relaxing without too much energy?",
    "What songs should I avoid if I want quiet acoustic music?",
]

# ---------------------------------------------------------------------------
# Fallback documentation corpus
# ---------------------------------------------------------------------------
# Each entry is a (topic, text) tuple. MusicBot indexes these when no
# external docs folder is present. "topic" replaces "filename" from DocuBot.

FALLBACK_DOCS = [
    # ── Full catalog ────────────────────────────────────────────────────────
    ("catalog", """Song catalog (20 songs):
1.  Sunrise City        | Artist: Neon Echo        | Genre: pop        | Mood: happy      | Energy: 0.82 | Acousticness: 0.18
2.  Midnight Coding     | Artist: LoRoom           | Genre: lofi       | Mood: chill      | Energy: 0.42 | Acousticness: 0.71
3.  Storm Runner        | Artist: Voltline         | Genre: rock       | Mood: intense    | Energy: 0.91 | Acousticness: 0.10
4.  Library Rain        | Artist: Paper Lanterns   | Genre: lofi       | Mood: chill      | Energy: 0.35 | Acousticness: 0.86
5.  Gym Hero            | Artist: Max Pulse        | Genre: pop        | Mood: intense    | Energy: 0.93 | Acousticness: 0.05
6.  Spacewalk Thoughts  | Artist: Orbit Bloom      | Genre: ambient    | Mood: chill      | Energy: 0.28 | Acousticness: 0.92
7.  Coffee Shop Stories | Artist: Slow Stereo      | Genre: jazz       | Mood: relaxed    | Energy: 0.37 | Acousticness: 0.89
8.  Night Drive Loop    | Artist: Neon Echo        | Genre: synthwave  | Mood: moody      | Energy: 0.75 | Acousticness: 0.22
9.  Focus Flow          | Artist: LoRoom           | Genre: lofi       | Mood: focused    | Energy: 0.40 | Acousticness: 0.78
10. Rooftop Lights      | Artist: Indigo Parade    | Genre: indie pop  | Mood: happy      | Energy: 0.76 | Acousticness: 0.35
11. Gold Chain Daydream | Artist: Westbound Sol    | Genre: hip-hop    | Mood: nostalgic  | Energy: 0.68 | Acousticness: 0.14
12. Velvet Underground Wish | Artist: Sable June   | Genre: r&b        | Mood: romantic   | Energy: 0.55 | Acousticness: 0.42
13. Moonlit Sonata      | Artist: Clara Voss       | Genre: classical  | Mood: dreamy     | Energy: 0.18 | Acousticness: 0.97
14. Cabin Smoke         | Artist: The Driftwood    | Genre: folk       | Mood: sad        | Energy: 0.31 | Acousticness: 0.91
15. Iron Cathedral      | Artist: Gravemass        | Genre: metal      | Mood: angry      | Energy: 0.96 | Acousticness: 0.04
16. Pulse Grid          | Artist: Synthex          | Genre: edm        | Mood: intense    | Energy: 0.94 | Acousticness: 0.03
17. Neon Petals         | Artist: Halo Drift       | Genre: dream pop  | Mood: dreamy     | Energy: 0.52 | Acousticness: 0.48
18. Broken Compass      | Artist: Rue Hollow       | Genre: indie folk | Mood: sad        | Energy: 0.34 | Acousticness: 0.88
19. Late Night Pickup   | Artist: Fader Kings      | Genre: r&b        | Mood: relaxed    | Energy: 0.48 | Acousticness: 0.33
20. Static Bloom        | Artist: Pale Circuit     | Genre: electronic | Mood: moody      | Energy: 0.72 | Acousticness: 0.11"""),

    # ── Highest energy songs ────────────────────────────────────────────────
    ("high_energy_songs", """Highest energy songs in the catalog (energy score 0.0–1.0, higher = more intense):
1. Iron Cathedral by Gravemass        — energy 0.96 — genre: metal    — mood: angry
2. Pulse Grid by Synthex              — energy 0.94 — genre: edm      — mood: intense
3. Gym Hero by Max Pulse              — energy 0.93 — genre: pop      — mood: intense
4. Storm Runner by Voltline           — energy 0.91 — genre: rock     — mood: intense
5. Sunrise City by Neon Echo          — energy 0.82 — genre: pop      — mood: happy
These songs are best for high-intensity activities like workouts or high-energy dance sessions."""),

    # ── Lofi genre ──────────────────────────────────────────────────────────
    ("lofi_genre", """Songs in the lofi genre:
- Midnight Coding by LoRoom      | Mood: chill   | Energy: 0.42 | Acousticness: 0.71
- Library Rain by Paper Lanterns | Mood: chill   | Energy: 0.35 | Acousticness: 0.86
- Focus Flow by LoRoom           | Mood: focused | Energy: 0.40 | Acousticness: 0.78
All three lofi songs have low energy (0.35–0.42) and high acousticness, making them ideal for studying, relaxing, or background listening."""),

    # ── Happy mood songs ────────────────────────────────────────────────────
    ("happy_mood", """Songs with a happy mood:
- Sunrise City by Neon Echo       | Genre: pop      | Energy: 0.82
- Rooftop Lights by Indigo Parade | Genre: indie pop | Energy: 0.76
These two songs are the only happy-mood tracks in the catalog. Sunrise City is more energetic; Rooftop Lights is slightly mellower."""),

    # ── Acoustic songs ──────────────────────────────────────────────────────
    ("acoustic_songs", """Most acoustic songs in the catalog (acousticness 0.0–1.0, higher = more acoustic):
1. Moonlit Sonata by Clara Voss       — acousticness 0.97 — genre: classical  — mood: dreamy
2. Spacewalk Thoughts by Orbit Bloom  — acousticness 0.92 — genre: ambient   — mood: chill
3. Cabin Smoke by The Driftwood       — acousticness 0.91 — genre: folk      — mood: sad
4. Coffee Shop Stories by Slow Stereo — acousticness 0.89 — genre: jazz      — mood: relaxed
5. Broken Compass by Rue Hollow       — acousticness 0.88 — genre: indie folk — mood: sad
6. Library Rain by Paper Lanterns     — acousticness 0.86 — genre: lofi      — mood: chill
7. Focus Flow by LoRoom               — acousticness 0.78 — genre: lofi      — mood: focused
Songs with acousticness above 0.70 are considered strongly acoustic."""),

    # ── Artists ─────────────────────────────────────────────────────────────
    ("artists", """Artists in the catalog and their songs:
- Neon Echo        : Sunrise City (pop/happy), Night Drive Loop (synthwave/moody)
- LoRoom           : Midnight Coding (lofi/chill), Focus Flow (lofi/focused)
- Voltline         : Storm Runner (rock/intense)
- Paper Lanterns   : Library Rain (lofi/chill)
- Max Pulse        : Gym Hero (pop/intense)
- Orbit Bloom      : Spacewalk Thoughts (ambient/chill)
- Slow Stereo      : Coffee Shop Stories (jazz/relaxed)
- Indigo Parade    : Rooftop Lights (indie pop/happy)
- Westbound Sol    : Gold Chain Daydream (hip-hop/nostalgic)
- Sable June       : Velvet Underground Wish (r&b/romantic)
- Clara Voss       : Moonlit Sonata (classical/dreamy)
- The Driftwood    : Cabin Smoke (folk/sad)
- Gravemass        : Iron Cathedral (metal/angry)
- Synthex          : Pulse Grid (edm/intense)
- Halo Drift       : Neon Petals (dream pop/dreamy)
- Rue Hollow       : Broken Compass (indie folk/sad)
- Fader Kings      : Late Night Pickup (r&b/relaxed)
- Pale Circuit     : Static Bloom (electronic/moody)"""),

    # ── Workout recommendation ───────────────────────────────────────────────
    ("workout", """Best songs for an intense workout (high energy, intense or angry mood):
1. Iron Cathedral by Gravemass  — energy 0.96 — metal/angry   — very heavy, maximum intensity
2. Pulse Grid by Synthex        — energy 0.94 — edm/intense   — driving electronic beat, great for cardio
3. Gym Hero by Max Pulse        — energy 0.93 — pop/intense   — upbeat and motivating, named for the gym
4. Storm Runner by Voltline     — energy 0.91 — rock/intense  — aggressive rock energy
These songs score highest for a user with high target_energy and intense mood preference."""),

    # ── Study / late night recommendation ───────────────────────────────────
    ("study_session", """Best songs for a late-night study session (low energy, focused or chill mood, high acousticness):
1. Focus Flow by LoRoom               — energy 0.40 — lofi/focused  — designed for concentration
2. Library Rain by Paper Lanterns     — energy 0.35 — lofi/chill    — very quiet, highly acoustic
3. Midnight Coding by LoRoom          — energy 0.42 — lofi/chill    — calm background beat for coding
4. Coffee Shop Stories by Slow Stereo — energy 0.37 — jazz/relaxed  — acoustic, ambient coffee-shop feel
5. Spacewalk Thoughts by Orbit Bloom  — energy 0.28 — ambient/chill — lowest energy in catalog, near-silent
These songs suit a profile with low target_energy, focused or chill mood, and likes_acoustic=True."""),

    # ── Chill acoustic recommendation ───────────────────────────────────────
    ("chill_acoustic", """Best songs for someone who likes chill, acoustic music (mood: chill or relaxed, high acousticness):
1. Library Rain by Paper Lanterns     — lofi/chill    — acousticness 0.86 — energy 0.35
2. Midnight Coding by LoRoom          — lofi/chill    — acousticness 0.71 — energy 0.42
3. Spacewalk Thoughts by Orbit Bloom  — ambient/chill — acousticness 0.92 — energy 0.28
4. Coffee Shop Stories by Slow Stereo — jazz/relaxed  — acousticness 0.89 — energy 0.37
5. Focus Flow by LoRoom               — lofi/focused  — acousticness 0.78 — energy 0.40
These tracks combine a calm mood with strong acoustic character."""),

    # ── High-energy pop recommendation ──────────────────────────────────────
    ("pop_lover", """Best songs for a high-energy pop lover (genre: pop or indie pop, high energy, happy or intense mood):
1. Gym Hero by Max Pulse           — pop/intense     — energy 0.93 — highest energy pop song
2. Sunrise City by Neon Echo       — pop/happy       — energy 0.82 — upbeat and bright
3. Rooftop Lights by Indigo Parade — indie pop/happy — energy 0.76 — feel-good indie pop
A pop fan with high target_energy will receive Gym Hero and Sunrise City at the top of their list.
Rooftop Lights appears when the mood target is happy rather than intense."""),
]


def load_fallback_documents():
    """
    Returns FALLBACK_DOCS as a list of (topic, text) tuples.
    Provided as a helper for environments where no docs/ folder is available.
    """
    return list(FALLBACK_DOCS)
