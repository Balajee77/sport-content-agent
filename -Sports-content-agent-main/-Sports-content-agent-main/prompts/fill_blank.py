
def get_fill_blank_prompt(sport, difficulty, context, previous_questions=""):
    return f"""
You are an expert sports trivia creator.

SPORT: {sport}
DIFFICULTY: {difficulty}

RETRIEVED CONTEXT:
{context}

PREVIOUS QUESTIONS:
{previous_questions}

Generate ONE fill-in-the-blank sports question.

Rules:
- Use only facts supported by context.
- Sentence must contain ____.
- Exactly 4 unique options.
- Exactly 1 correct answer.
- Avoid repeating previous content.
- Include a short explanation.
- Include source title and URL.

Return JSON only:

{{
  "type": "Fill in the Blank",
  "sport": "{sport}",
  "difficulty": "{difficulty}",
  "sentence": "... ____ ...",
  "options": ["...", "...", "...", "..."],
  "correct_answer": "...",
  "explanation": "...",
  "source_title": "...",
  "source_url": "..."
}}
"""
