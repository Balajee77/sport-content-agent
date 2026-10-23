
def get_mcq_prompt(sport, difficulty, context, previous_questions=""):
    return f"""
You are an expert sports quiz creator.

SPORT: {sport}
DIFFICULTY: {difficulty}

RETRIEVED CONTEXT:
{context}

PREVIOUS QUESTIONS:
{previous_questions}

Generate ONE Instagram-friendly MCQ.

Rules:
- Use only facts supported by the retrieved context.
- Exactly 4 unique options.
- Exactly 1 correct answer.
- Keep the question concise.
- Avoid repeating previous questions.
- Explanation must be short.
- Include the source title and source URL from the context.

Return valid JSON only in this format:

{{
  "type": "MCQ",
  "sport": "{sport}",
  "difficulty": "{difficulty}",
  "question": "...",
  "options": ["...", "...", "...", "..."],
  "correct_answer": "...",
  "explanation": "...",
  "source_title": "...",
  "source_url": "..."
}}
"""
