
def get_true_false_prompt(sport, difficulty, context, previous_questions=""):
    return f"""
You are an expert sports fact checker.

SPORT: {sport}
DIFFICULTY: {difficulty}

RETRIEVED CONTEXT:
{context}

PREVIOUS QUESTIONS:
{previous_questions}

Generate ONE True/False sports challenge.

Rules:
- Use only facts supported by retrieved context.
- Do not invent facts.
- correct_answer must be true or false.
- Keep the statement concise.
- Avoid repeating previous content.
- Include a short explanation.
- Include source title and URL.

Return JSON only:

{{
  "type": "True/False",
  "sport": "{sport}",
  "difficulty": "{difficulty}",
  "statement": "...",
  "correct_answer": true,
  "explanation": "...",
  "source_title": "...",
  "source_url": "..."
}}
"""
