# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**1. Catalog genre imbalance ("lofi privilege").** The catalog has three lofi songs but only one each for metal, jazz, edm, and classical. A lofi user will always have their top three slots filled by exact genre matches, while a metal or edm user gets only one strong result before the system falls back on energy proximity to fill the rest. This is not a flaw in the scoring formula — it is a data problem — but the formula has no way to compensate for it, so some users consistently receive worse recommendations than others purely because of how the dataset was built.

**2. Single-song genre trap.** The most visible version of the imbalance above shows up at the extreme. When the adversarial "metal / angry" profile was tested, *Iron Cathedral* scored a near-perfect 5.98 at position #1 — but positions #2 through #5 dropped to around 3.2, a gap of nearly 2.8 points. Those remaining slots were filled not by musically related songs but by whichever high-energy tracks happened to share an adjacent mood tag, regardless of how different they actually sound. The system has no way to signal to the user that it ran out of relevant options — it silently serves a degraded playlist as if nothing changed.

**3. Energy scores never reach zero.** The energy scoring formula uses a squared distance penalty, which sounds fair — but because the catalog only spans an energy range of 0.18 to 0.96, the maximum possible distance between a user's target and any song is 0.78. At that worst case, the formula still awards 0.78 points out of a possible 2.0. This means every song always earns some energy credit, so completely irrelevant songs can drift into the top 5 on energy alone when genre and mood both miss. Nothing is ever truly filtered out.

**4. High-energy users get fewer good matches.** The catalog is skewed toward lower-energy songs — nine songs sit below 0.5 energy, while only four are above 0.85. A user targeting energy 0.4 has seven songs within close range; a user targeting energy 0.9 has only four. Low-energy users get consistently higher energy scores across the board simply because more songs happen to cluster near them in the catalog. This is an invisible advantage that has nothing to do with how well the system understands their taste.

**5. Genre matching is all-or-nothing with no cultural adjacency.** A pop fan gets zero genre points from an indie pop song, zero from a dream pop song, and zero from a synthwave song — even though all three are culturally and sonically close. Mood matching has a partial-credit system for adjacent vibes, but genre has no equivalent. A miss on genre is treated the same whether the gap is pop-to-metal (very different) or pop-to-indie pop (nearly the same thing), which means the system is less accurate for users whose preferred genre sits close to another genre in the catalog.

**6. The mood neighbor map only travels in one direction.** The adjacency map that allows partial credit for similar moods was built entry by entry and is not symmetric. A sad user can discover moody songs and receive +0.75 for them, but a moody user cannot discover sad songs — the connection only exists in one direction. Similarly, a focused user can find chill songs, but the reverse path has different neighbors. Users with moods that have fewer or weaker neighbors receive less partial credit than users whose moods are more richly connected, which affects ranking in ways that are invisible from the outside.

**7. Tie-breaking always favors happier songs.** When two songs score identically, the system picks whichever has higher valence — a measure of musical positivity. This means a sad or moody user will always lose ties to upbeat songs, even when their stated preference is for low-energy, low-valence music. The tie-breaker was intended as a neutral default but it introduces a systematic preference for cheerful-sounding songs regardless of the user's actual mood.

**8. No diversity — the same songs always win.** There is no mechanism to spread recommendations across different artists, genres, or sounds. A lofi user will always see the same three lofi songs in the same top three positions on every run. Two songs from the same artist can both appear in a single top-five list. In a real music app this would create a filter bubble — the system keeps confirming what it already knows about you rather than helping you discover anything new. The scoring formula optimizes purely for closeness to the stated profile, with nothing to reward variety or surprise.

**9. A single profile cannot capture context-switching listeners.** Every user is represented by one genre, one mood, one energy target, and one acoustic preference. A person who listens to intense metal at the gym and quiet folk in the evening is forced to choose one context and gets a compromise playlist that serves neither well. Real listening behavior shifts with time of day, activity, and emotional state — the static profile has no way to represent that, which means the system structurally underserves anyone whose taste is not uniform across all situations.

---

## 7. Evaluation  

Ten user profiles were run in total — five standard profiles covering common listening contexts, and five adversarial profiles designed to break the system in specific ways.

**Standard profiles tested:**
- *High-Energy Pop* — a person who wants upbeat pop music for a happy occasion (energy 0.85, genre pop, mood happy)
- *Chill Lofi* — a late-night study session with quiet, focused, acoustic-leaning music (energy 0.40, genre lofi, mood focused)
- *Deep Intense Rock* — aggressive, loud rock for a workout or driving (energy 0.90, genre rock, mood intense)
- *Melancholic Evening* — slow, sad, acoustic folk for a quiet night in (energy 0.30, genre folk, mood sad)
- *Friday Night EDM* — high-energy electronic music for dancing (energy 0.92, genre edm, mood intense)

**Adversarial profiles tested:**
- *Conflicting Energy vs Mood* — asked for sad rock at high energy, two signals pointing in opposite directions
- *Single-Song Genre* — asked for metal, a genre with only one song in the catalog
- *Dead-Center Energy* — asked for jazz at exactly 0.5 energy, where most songs score similarly on energy
- *Acoustic + High Energy Contradiction* — asked for folk with acoustic preference but high energy target, which almost no song can satisfy
- *No Catalog Match* — asked for classical and angry, a combination that does not exist in the catalog at all

**What the results showed:**

Every standard profile returned a sensible #1 result — the song that matched genre, mood, and energy all at once always won by a large margin. *Focus Flow* for lofi, *Storm Runner* for rock, *Cabin Smoke* for folk. The system worked as designed in clean, non-conflicting cases.

**What surprised me — and why Gym Hero keeps showing up:**

*Gym Hero* appeared in the top 5 for three different profiles: High-Energy Pop, Deep Intense Rock, and Friday Night EDM. At first glance it seems odd that a gym-energy pop song would show up for a rock fan or an EDM fan. But the reason makes sense once you understand how the scoring works.

Imagine you are looking for happy pop music. The system goes through every song and gives it points in four categories. *Gym Hero* is a pop song, so it gets full marks for genre — that is worth 2 out of 6 possible points right away, the single biggest chunk. Its energy level (0.93) is extremely close to your target (0.85), so it scores nearly perfectly on energy too — another 2 points. Together those two things give it almost 4 points before mood or acoustics are even considered. The fact that *Gym Hero* is tagged "intense" rather than "happy" costs it 1.5 points, but it still ends up at 4.46 out of 6 — easily enough for #2. The system is not wrong in a technical sense: *Gym Hero* really is a pop song that matches your energy target very well. But it cannot tell the difference between a birthday party playlist and a pre-workout playlist. Both are "high-energy pop" by the numbers.

For a rock fan, *Gym Hero* appears for a different reason: the rock profile wants "intense" music, and *Gym Hero* is tagged intense. It gets the full 1.5 mood points plus nearly perfect energy points, and since there is only one rock song in the catalog, the other slots go to the next-best energy + mood combinations — which *Gym Hero* satisfies better than most. It is the system falling back to what it can measure when it runs out of exact genre matches.

**Surprising finding from adversarial tests:**

The most unexpected result came from the "No Catalog Match" profile (classical + angry). The system returned *Moonlit Sonata* (a classical piece) at #1 because the genre match (+2.0) outweighed the mood match (+1.5). A real classical music fan would likely be baffled to see *Iron Cathedral* by Gravemass — a metal song — at #2 on a classical profile, but the formula considered it a reasonable suggestion because it matched the "angry" mood and had decent energy. The system was technically correct but intuitively wrong, and there was nothing in the output to explain that both primary preferences had failed simultaneously.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
