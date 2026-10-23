
import json
import re

from google import genai

from prompts.batch_prompt import get_batch_prompt

from retrieval.web_search import (
    search_sports_web,
    format_web_context
)

from retrieval.chroma_retriever import (
    search_chroma,
    format_chroma_context
)

from schemas.content_models import (
    MCQItem,
    TrueFalseItem,
    PollItem,
    FillBlankItem,
    GuessNumberItem
)

from utils.history import (
    get_previous_questions,
    save_item_to_history,
    is_duplicate_item
)


MODEL_NAME = "gemini-3.6-flash"


def clean_json(text):
    text = text.strip()

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


def validate_item(item):
    """
    Normalize small LLM field variations, then validate
    against the correct Pydantic schema.
    """

    content_type = item.get("type")

    # -------------------------
    # MCQ
    # -------------------------
    if content_type == "MCQ":

        if "question" not in item and "statement" in item:
            item["question"] = item["statement"]

        return MCQItem(**item).model_dump()


    # -------------------------
    # TRUE / FALSE
    # -------------------------
    elif content_type == "True/False":

        # Gemini may occasionally return "question"
        # instead of "statement".
        if "statement" not in item:

            if "question" in item:
                item["statement"] = item["question"]

            elif "prompt" in item:
                item["statement"] = item["prompt"]

        return TrueFalseItem(**item).model_dump()


    # -------------------------
    # POLL
    # -------------------------
    elif content_type == "Poll":

        if "prompt" not in item:

            if "question" in item:
                item["prompt"] = item["question"]

            elif "statement" in item:
                item["prompt"] = item["statement"]

        item["opinion_based"] = True
        item["grounding_source"] = "Opinion"

        return PollItem(**item).model_dump()


    # -------------------------
    # FILL IN THE BLANK
    # -------------------------
    elif content_type == "Fill in the Blank":

        if "sentence" not in item:

            if "question" in item:
                item["sentence"] = item["question"]

            elif "statement" in item:
                item["sentence"] = item["statement"]

        return FillBlankItem(**item).model_dump()


    # -------------------------
    # GUESS THE NUMBER
    # -------------------------
    elif content_type == "Guess the Number":

        if "question" not in item:

            if "statement" in item:
                item["question"] = item["statement"]

            elif "prompt" in item:
                item["question"] = item["prompt"]

        # Gemini may occasionally return tolerance=0.
        # Schema requires tolerance to be greater than 0.
        tolerance = item.get("tolerance")

        if tolerance is None or tolerance <= 0:
            item["tolerance"] = 1

        return GuessNumberItem(**item).model_dump()


    else:
        raise ValueError(
            f"Unsupported content type: {content_type}"
        )

def build_combined_context(
    tavily_api_key,
    sport
):
    web_query = (
        f"{sport} latest official results records statistics "
        f"tournaments major players verified facts"
    )

    web_results = search_sports_web(
        api_key=tavily_api_key,
        sport=sport,
        query=web_query,
        max_results=5
    )

    web_context = format_web_context(
        web_results
    )

    chroma_results = search_chroma(
        sport=sport,
        query=f"{sport} historical records rules tournaments milestones",
        n_results=5
    )

    chroma_context = format_chroma_context(
        chroma_results
    )

    return f"""
WEB SEARCH CONTEXT:
{web_context}

CHROMADB HISTORICAL CONTEXT:
{chroma_context}
"""


def generate_batch(
    gemini_api_key,
    tavily_api_key,
    sport,
    difficulty,
    selected_types,
    batch_size=4
):
    """
    Generate a full 4–5 item batch using ONE Gemini request.
    """

    if batch_size not in [4, 5]:
        raise ValueError(
            "Batch size must be 4 or 5."
        )

    if not selected_types:
        raise ValueError(
            "Select at least one content type."
        )

    context = build_combined_context(
        tavily_api_key=tavily_api_key,
        sport=sport
    )

    previous_questions = get_previous_questions(
        sport=sport,
        limit=30
    )

    prompt = get_batch_prompt(
        sport=sport,
        difficulty=difficulty,
        selected_types=selected_types,
        batch_size=batch_size,
        context=context,
        previous_questions=previous_questions
    )

    client = genai.Client(
        api_key=gemini_api_key
    )

    model_candidates = [
        "gemini-3.5-flash-lite",
        "gemini-3.5-flash",
        "gemini-3.7-flash",
        "gemini-3.6-flash"
    ]

    response = None
    last_error = None

    for model_name in model_candidates:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            break

        except Exception as error:
            last_error = error

            error_text = str(error)

            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            ):
                continue

            raise

    if response is None:
        raise ValueError(
            f"All Gemini fallback models failed. Last error: {last_error}"
        )

    if not response.text:
        raise ValueError(
            "Gemini returned empty response."
        )

    cleaned = clean_json(
        response.text
    )

    try:
        raw_items = json.loads(
            cleaned
        )

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Gemini returned invalid JSON.\n\n"
            f"{response.text}"
        ) from error

    if not isinstance(raw_items, list):
        raise ValueError(
            "Gemini response must be a JSON array."
        )

    if len(raw_items) != batch_size:
        raise ValueError(
            f"Expected {batch_size} items, "
            f"but Gemini returned {len(raw_items)}."
        )

    validated_items = []

    for raw_item in raw_items:

        validated = validate_item(
            raw_item
        )

        # Diversity is encouraged through previous-question prompting.
        # Do not fail the entire regenerated batch because one item is
        # semantically similar to historical content.
        validated_items.append(
            validated
        )

    for item in validated_items:
        save_item_to_history(item)

    return validated_items
