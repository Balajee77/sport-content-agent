
import json
import re
import time

from google import genai

from prompts.mcq import get_mcq_prompt
from prompts.true_false import get_true_false_prompt
from prompts.poll import get_poll_prompt
from prompts.fill_blank import get_fill_blank_prompt
from prompts.guess_number import get_guess_number_prompt

from schemas.content_models import (
    MCQItem,
    TrueFalseItem,
    PollItem,
    FillBlankItem,
    GuessNumberItem
)


MODEL_NAME = "gemini-3.6-flash"


def clean_json_response(text: str):
    """
    Remove markdown code fences if Gemini returns JSON inside ```json blocks.
    """

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


def call_gemini(api_key: str, prompt: str):
    """
    Call Gemini and parse JSON response.
    """

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    cleaned_text = clean_json_response(response.text)

    try:
        return json.loads(cleaned_text)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Gemini did not return valid JSON.\n\n"
            f"Raw response:\n{response.text}"
        ) from error


def validate_item(content_type: str, data: dict):
    """
    Validate generated output against its type-specific Pydantic schema.
    """

    if content_type == "MCQ":
        return MCQItem(**data).model_dump()

    elif content_type == "True/False":
        return TrueFalseItem(**data).model_dump()

    elif content_type == "Poll":
        return PollItem(**data).model_dump()

    elif content_type == "Fill in the Blank":
        return FillBlankItem(**data).model_dump()

    elif content_type == "Guess the Number":
        return GuessNumberItem(**data).model_dump()

    else:
        raise ValueError(
            f"Unsupported content type: {content_type}"
        )


def build_prompt(
    content_type,
    sport,
    difficulty,
    context,
    previous_questions=""
):
    """
    Select the correct type-specific prompt template.
    """

    if content_type == "MCQ":
        return get_mcq_prompt(
            sport,
            difficulty,
            context,
            previous_questions
        )

    elif content_type == "True/False":
        return get_true_false_prompt(
            sport,
            difficulty,
            context,
            previous_questions
        )

    elif content_type == "Poll":
        return get_poll_prompt(
            sport,
            previous_questions
        )

    elif content_type == "Fill in the Blank":
        return get_fill_blank_prompt(
            sport,
            difficulty,
            context,
            previous_questions
        )

    elif content_type == "Guess the Number":
        return get_guess_number_prompt(
            sport,
            difficulty,
            context,
            previous_questions
        )

    else:
        raise ValueError(
            f"Unsupported content type: {content_type}"
        )


def generate_content_item(
    api_key,
    sport,
    difficulty,
    content_type,
    context="",
    previous_questions="",
    max_retries=2
):
    """
    Generate one validated sports content item.

    If Gemini returns invalid JSON or schema-invalid output,
    retry automatically.
    """

    prompt = build_prompt(
        content_type=content_type,
        sport=sport,
        difficulty=difficulty,
        context=context,
        previous_questions=previous_questions
    )

    last_error = None

    for attempt in range(max_retries + 1):

        try:
            raw_data = call_gemini(
                api_key=api_key,
                prompt=prompt
            )

            validated_data = validate_item(
                content_type=content_type,
                data=raw_data
            )

            return validated_data

        except Exception as error:
            last_error = error

            error_text = str(error)

            # Handle Gemini free-tier rate limit
            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                print("Gemini rate limit reached. Waiting 30 seconds...")
                time.sleep(30)
                continue

            prompt += f"""

IMPORTANT:
Your previous response failed validation.

Validation error:
{str(error)}

Return ONLY valid JSON matching the exact required schema.
"""

    raise ValueError(
        f"Generation failed after retries.\n"
        f"Last error: {last_error}"
    )
