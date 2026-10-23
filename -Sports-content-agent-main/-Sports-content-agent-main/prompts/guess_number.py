
def get_guess_number_prompt(sport, difficulty, context, previous_questions=""):
    return f"""
You are an expert sports statistics quiz creator.

SPORT: {sport}
DIFFICULTY: {difficulty}

RETRIEVED CONTEXT:
{context}

PREVIOUS QUESTIONS:
{previous_questions}

Generate ONE Guess-the-Number challenge.

Rules:
- Ask about a numeric sports fact.
- The target number must be supported by context.
- Do not estimate or invent values.
- target_number must be numeric.
- tolerance must be greater than 0.
- Avoid repeating previous questions.
- Include a short explanation.
- Include source title and URL.

Return JSON only:

{{
  "type": "Guess the Number",
  "sport": "{sport}",
  "difficulty": "{difficulty}",
  "question": "...",
  "target_number": 100,
  "tolerance": 5,
  "explanation": "...",
  "source_title": "...",
  "source_url": "..."
}}
"""
