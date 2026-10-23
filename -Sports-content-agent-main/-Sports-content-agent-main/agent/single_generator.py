
import json
import re

from google import genai

from agent.content_agent import (
    build_prompt,
    validate_item
)

from retrieval.web_search import (
    search_sports_web,
    format_web_context
)

from retrieval.chroma_retriever import (
    search_chroma,
    format_chroma_context
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


def generate_one_item(
    gemini_api_key,
    tavily_api_key,
    sport,
    difficulty,
    content_type
):

    previous = get_previous_questions(
        sport=sport,
        limit=25
    )

    if content_type == "Poll":
        context = ""

    else:
        web_results = search_sports_web(
            api_key=tavily_api_key,
            sport=sport,
            query=(
                f"{sport} official records results "
                f"statistics tournaments facts"
            ),
            max_results=4
        )

        web_context = format_web_context(
            web_results
        )

        chroma_results = search_chroma(
            sport=sport,
            query=f"{sport} historical facts records",
            n_results=4
        )

        chroma_context = format_chroma_context(
            chroma_results
        )

        context = f"""
WEB:
{web_context}

CHROMADB:
{chroma_context}
"""

    prompt = build_prompt(
        content_type=content_type,
        sport=sport,
        difficulty=difficulty,
        context=context,
        previous_questions=previous
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
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
                or "503" in error_text
                or "UNAVAILABLE" in error_text
                or "404" in error_text
            ):
                continue

            raise

    if response is None:
        raise ValueError(
            f"All Gemini models failed. Last error: {last_error}"
        )

    if not response.text:
        raise ValueError(
            "Gemini returned empty response."
        )

    data = json.loads(
        clean_json(response.text)
    )

    validated = validate_item(
        content_type,
        data
    )

    # Diversity is encouraged through previous-question prompting.
    # Do not fail regeneration just because the new item is
    # semantically similar to earlier content.

    save_item_to_history(
        validated
    )

    return validated
