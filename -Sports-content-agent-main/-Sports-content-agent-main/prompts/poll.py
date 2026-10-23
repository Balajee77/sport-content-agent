
def get_poll_prompt(sport, previous_questions=""):
    return f"""
You are a creative sports social media content creator.

SPORT: {sport}

PREVIOUS POLLS:
{previous_questions}

Generate ONE engaging This-or-That sports poll.

Rules:
- Exactly 2 options.
- No correct answer.
- Opinion based only.
- Keep it Instagram-friendly.
- Both choices should be reasonable.
- Avoid repeating previous polls.

Return JSON only:

{{
  "type": "Poll",
  "sport": "{sport}",
  "prompt": "...",
  "options": ["...", "..."],
  "opinion_based": true
}}
"""
