# Reflection: Profile Pair Comparisons

For each pair of profiles, this file notes what changed between their outputs, why it makes sense given the scoring logic, and what it reveals about what the system actually measures.

---

## Pair 1: High-Energy Pop vs Deep Intense Rock

**Profiles compared:**
- High-Energy Pop: genre=pop, mood=happy, energy=0.85, no acoustic
- Deep Intense Rock: genre=rock, mood=intense, energy=0.90, no acoustic

**What changed:**
Both profiles want high energy and no acoustic texture, but they returned completely different top-5 lists. *Sunrise City* was #1 for pop and nowhere near the top for rock. *Storm Runner* was #1 for rock and did not appear for pop at all. However, *Gym Hero* appeared in both lists — it was #2 for pop and #3 for rock.

**Why it makes sense:**
The two profiles are close on energy but far apart on genre and mood. *Sunrise City* (pop, happy, 0.82) is a near-perfect pop/happy match so it dominates the pop list, but a rock fan gets zero genre points from it — it simply disappears. *Storm Runner* (rock, intense, 0.91) is the mirror image: perfect for rock, invisible to pop.

*Gym Hero* is the interesting overlap. For the pop user it earns genre points (it is a pop song) even though the mood is wrong. For the rock user it earns mood points (it is tagged intense, which the rock profile wants) even though the genre is wrong. Different reasons, same result — it ends up in both lists because it partially satisfies each profile through a different scoring path. This is a sign that the four-feature scoring creates overlapping zones: two very different users can agree on a song for completely different reasons.

---

## Pair 2: Chill Lofi vs Melancholic Evening

**Profiles compared:**
- Chill Lofi: genre=lofi, mood=focused, energy=0.40, acoustic=yes
- Melancholic Evening: genre=folk, mood=sad, energy=0.30, acoustic=yes

**What changed:**
Both profiles want quiet, acoustic music at low energy. Yet their top-5 lists share zero songs. Lofi's top 3 were all lofi songs (*Focus Flow*, *Library Rain*, *Midnight Coding*). Folk's top 2 were folk-adjacent (*Cabin Smoke*, *Broken Compass*), then three completely different songs filled positions 3–5.

**Why it makes sense:**
These two profiles are neighbors in energy and acoustic space but very different in genre and mood. The genre weight (+2.0) is strong enough to fully separate them even when everything else is similar. A lofi fan rewards three lofi songs before any other genre gets a look in. A folk fan exhausts their genre options after two songs (*Cabin Smoke* and *Broken Compass*), then the system falls back to energy proximity — which is why positions 3–5 look random: *Spacewalk Thoughts*, *Moonlit Sonata*, and *Night Drive Loop* all scored similarly on energy against the 0.30 target with no genre or mood help.

The takeaway: when two users have similar numbers (energy, acoustic) but different category labels (genre, mood), their playlists will look almost completely unrelated. The category labels do more heavy lifting than the continuous numbers in typical cases.

---

## Pair 3: Friday Night EDM vs EDGE: Single-Song Genre (Metal)

**Profiles compared:**
- Friday Night EDM: genre=edm, mood=intense, energy=0.92, no acoustic
- EDGE: Single-Song Genre: genre=metal, mood=angry, energy=0.95, no acoustic

**What changed:**
Both profiles target the highest-energy region of the catalog and want aggressive, intense music. But the EDM profile got a cohesive top 5 (Pulse Grid dominating, then three intense songs close behind), while the metal profile got a single dominant #1 (*Iron Cathedral* at 5.98) followed by a sharp drop to three songs scoring around 3.2.

**Why it makes sense:**
The EDM profile benefits from having an "intense" mood that connects to three other songs via exact or adjacent mood matches — *Gym Hero*, *Storm Runner*, and *Pulse Grid* all tag intense. The metal profile's "angry" mood is narrower: only *Iron Cathedral* matches it, and the only adjacent mood is "intense," which then connects to the same high-energy cluster. The songs are similar, but for the metal fan they feel like poor substitutes because the genre is completely wrong — the system cannot express that gap. Both profiles end up with Pulse Grid, Gym Hero, and Storm Runner in their lower positions, but for the EDM fan those are reasonable fallbacks; for the metal fan they are a mismatch that the system is powerless to flag.

---

## Pair 4: EDGE: Conflicting Energy vs Mood vs EDGE: Acoustic + High Energy Contradiction

**Profiles compared:**
- Conflicting Energy vs Mood: genre=rock, mood=sad, energy=0.90, no acoustic
- Acoustic + High Energy Contradiction: genre=folk, mood=intense, energy=0.90, acoustic=yes

**What changed:**
Both profiles contain a contradiction — one wants sad music at high energy, the other wants acoustic music at high energy. But they resolved differently. The conflicting profile clearly picked energy over mood: *Storm Runner* (no mood match) ranked #1 well ahead of the sad songs. The contradiction profile got compressed, nearly tied scores in the 3.5–3.8 range with no clear winner.

**Why it makes sense:**
In the conflicting profile, energy and genre reinforce each other — rock + high energy points toward the same songs. Mood is the lonely dissenting signal. When two features agree and one disagrees, the two win. That is a decisive outcome.

In the contradiction profile, all four features pull in different directions. High energy points toward loud electronic songs. Acoustic preference points toward quiet folk songs. Genre (folk) points toward low-energy acoustic songs. Mood (intense) points toward high-energy electronic songs. Every candidate song satisfies some of these and violates others, so they all end up with similar middle-ground scores. The system cannot find a winner because none exists — no song in the catalog is both high-energy and highly acoustic. The compressed scores (3.5 to 3.8, a range of just 0.3) are the system's way of expressing that it is guessing, though it never says so out loud.

---

## Pair 5: EDGE: Dead-Center Energy vs EDGE: No Catalog Match (Classical + Angry)

**Profiles compared:**
- Dead-Center Energy: genre=jazz, mood=relaxed, energy=0.50, acoustic=yes
- No Catalog Match: genre=classical, mood=angry, energy=0.50, no acoustic

**What changed:**
Both profiles ask for energy=0.50, which is the middle of the catalog's range. Yet one produced a clean, intuitive ranking and the other produced incoherent results. *Coffee Shop Stories* (jazz, relaxed, 0.37 energy) won the jazz profile with a strong 5.91 score. *Moonlit Sonata* (classical, dreamy) won the classical profile with only 3.81, followed by *Iron Cathedral* (metal, angry) at 3.56.

**Why it makes sense:**
With energy set to 0.50, almost every song in the catalog scores similarly on the energy component — differences between songs are small. That means genre and mood become the deciding factors, because they create large point gaps (2.0 for genre, 1.5 for mood) while energy differences are fractions of a point.

For the jazz profile, this is fine — *Coffee Shop Stories* matches both genre and mood, so it leaps ahead regardless of a slight energy offset. The genre and mood signals are doing their job.

For the classical/angry profile, the problem is that no song satisfies both. *Moonlit Sonata* wins genre but has zero mood match. *Iron Cathedral* wins mood but has zero genre match. Neither can accumulate both +2.0 and +1.5 simultaneously. The result is a list where the top two songs are fundamentally different (a gentle classical piece and a death metal track) ranked almost equally, because the scoring formula can only compare their partial scores — it has no way to say "both of these are wrong for this user." Dead-center energy revealed that the system's stability depends entirely on whether the categorical signals (genre, mood) are reliable. When they are, it works well. When they both fail at once, it breaks quietly.
