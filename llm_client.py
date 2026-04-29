"""
Gemini client wrapper used by MusicBot.

Handles:
- Configuring the Gemini client from the GEMINI_API_KEY environment variable
- Naive "generation only" answers over the full docs corpus (Phase 0)
- RAG style answers that use only retrieved snippets (Phase 2)
"""

import os
import logging
from google import genai

logger = logging.getLogger("musicbot.llm")

GEMINI_MODEL_NAME = "gemini-2.5-flash"


class GeminiClient:
    """
    Simple wrapper around the Gemini model.

    Usage:
        client = GeminiClient()
        answer = client.naive_answer_over_full_docs(query, all_text)
        # or
        answer = client.answer_from_snippets(query, snippets)
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "Missing GEMINI_API_KEY environment variable. "
                "Set it in your shell or .env file to enable LLM features."
            )
        self.client = genai.Client(api_key=api_key)
        logger.info("GeminiClient initialized with model '%s'", GEMINI_MODEL_NAME)

    # -----------------------------------------------------------
    # Phase 0: naive generation over full docs
    # -----------------------------------------------------------

    def naive_answer_over_full_docs(self, query, all_text):
        """Send the full corpus and query to the LLM with no retrieval filtering."""
        logger.info("Naive LLM call | query=%r | corpus_chars=%d", query, len(all_text))
        prompt = f"""You are a music assistant with access to a song catalog.
Answer the following question using the catalog information provided.

Catalog:
{all_text}

Question: {query}
"""
        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL_NAME,
                contents=prompt,
            )
            result = (response.text or "").strip()
            logger.info("Naive LLM response received (%d chars)", len(result))
            return result
        except Exception as exc:
            logger.error("Naive LLM call failed: %s", exc)
            raise

    # -----------------------------------------------------------
    # Phase 2: RAG style generation over retrieved snippets
    # -----------------------------------------------------------

    def answer_from_snippets(self, query, snippets):
        """Generate an answer using only the retrieved snippets."""
        if not snippets:
            return "I do not know based on the docs I have."

        logger.info("RAG LLM call | query=%r | snippets=%d", query, len(snippets))

        context_blocks = []
        for topic, text in snippets:
            context_blocks.append(f"Topic: {topic}\n{text}\n")

        context = "\n\n".join(context_blocks)

        prompt = f"""You are a cautious music assistant.

You will receive:
- A question about the music catalog
- A small set of relevant snippets from the catalog documentation

Your job:
- Answer the question using only the information in the snippets.
- If the snippets do not provide enough evidence, refuse to guess.

Snippets:
{context}

Question:
{query}

Rules:
- Use only the information in the snippets. Do not invent songs, artists, or attributes.
- If the snippets are not enough to answer confidently, reply exactly:
  "I do not know based on the docs I have."
- When you do answer, briefly mention which topic you relied on.
"""
        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL_NAME,
                contents=prompt,
            )
            result = (response.text or "").strip()
            logger.info("RAG LLM response received (%d chars)", len(result))
            return result
        except Exception as exc:
            logger.error("RAG LLM call failed: %s", exc)
            raise
