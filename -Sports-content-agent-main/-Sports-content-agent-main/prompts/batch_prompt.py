
def get_batch_prompt(
    sport,
    difficulty,
    selected_types,
    batch_size,
    context,
    previous_questions=""
):
    return f"""
You are an expert sports engagement content agent.

SPORT:
{sport}

DIFFICULTY:
{difficulty}

ALLOWED CONTENT TYPES:
{selected_types}

BATCH SIZE:
{batch_size}

RETRIEVED FACTUAL CONTEXT:
{context}

PREVIOUSLY GENERATED CONTENT:
{previous_questions}

Generate exactly {batch_size} Instagram-ready sports engagement items.

IMPORTANT:
- Only use content types from ALLOWED CONTENT TYPES.
- Mix types when multiple types are provided.
- Factual items must use ONLY facts supported by retrieved context.
- Do not invent statistics, scores, players, dates, records or tournament outcomes.
- Polls are opinion-based and do not need factual grounding.
- Avoid repeating previous questions or the same fact inside this batch.
- Every factual item must include source_title and source_url copied from the retrieved context.
- Every factual item must include grounding_source.
- Set grounding_source to "Web Search" when the supporting fact comes from WEB SEARCH CONTEXT.
- Set grounding_source to "ChromaDB" when the supporting fact comes from CHROMADB HISTORICAL CONTEXT.
- Never claim ChromaDB grounding if the fact came from web context.
- Poll items must use grounding_source = "Opinion".

TYPE RULES:

MCQ:
- type must be "MCQ"
- exactly 4 unique options
- exactly 1 correct answer
- correct_answer must exactly match one option
- short explanation

True/False:
- type must be "True/False"
- factual statement
- correct_answer must be true or false
- short explanation

Poll:
- type must be "Poll"
- exactly 2 options
- opinion_based must be true
- no correct answer
- do not include source fields

Fill in the Blank:
- type must be "Fill in the Blank"
- sentence must contain ____
- exactly 4 unique options
- exactly 1 correct answer
- short explanation

Guess the Number:
- type must be "Guess the Number"
- target_number must be numeric
- tolerance must be numeric and greater than 0
- short explanation

Return ONLY a valid JSON array.
Do not use markdown.
Do not use ```json.

Example structure:

[
  {{
    "type": "MCQ",
    "sport": "{sport}",
    "difficulty": "{difficulty}",
    "question": "...",
    "options": ["...", "...", "...", "..."],
    "correct_answer": "...",
    "explanation": "...",
    "source_title": "...",
    "source_url": "...",
    "grounding_source": "Web Search"
  }},
  {{
    "type": "Poll",
    "sport": "{sport}",
    "prompt": "...",
    "options": ["...", "..."],
    "opinion_based": true,
    "grounding_source": "Opinion"
  }}
]
"""
