
from typing import Literal
from pydantic import BaseModel, Field, field_validator


class MCQItem(BaseModel):
    type: Literal["MCQ"] = "MCQ"
    sport: str
    difficulty: Literal["Easy", "Medium", "Hard"]
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str
    source_title: str | None = None
    source_url: str | None = None
    grounding_source: str | None = None

    @field_validator("options")
    @classmethod
    def validate_options(cls, value):
        if len(value) != 4:
            raise ValueError("MCQ must contain exactly 4 options.")

        if len(set(value)) != 4:
            raise ValueError("MCQ options must be unique.")

        return value


class TrueFalseItem(BaseModel):
    type: Literal["True/False"] = "True/False"
    sport: str
    difficulty: Literal["Easy", "Medium", "Hard"]
    statement: str
    correct_answer: bool
    explanation: str
    source_title: str | None = None
    source_url: str | None = None
    grounding_source: str | None = None


class PollItem(BaseModel):
    type: Literal["Poll"] = "Poll"
    sport: str
    prompt: str
    options: list[str] = Field(min_length=2, max_length=2)
    opinion_based: bool = True
    grounding_source: str = "Opinion"

    @field_validator("options")
    @classmethod
    def validate_poll_options(cls, value):
        if len(value) != 2:
            raise ValueError("Poll must contain exactly 2 options.")

        if len(set(value)) != 2:
            raise ValueError("Poll options must be different.")

        return value


class FillBlankItem(BaseModel):
    type: Literal["Fill in the Blank"] = "Fill in the Blank"
    sport: str
    difficulty: Literal["Easy", "Medium", "Hard"]
    sentence: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str
    source_title: str | None = None
    source_url: str | None = None
    grounding_source: str | None = None

    @field_validator("sentence")
    @classmethod
    def validate_blank(cls, value):
        if "____" not in value:
            raise ValueError("Sentence must contain ____ as the blank.")
        return value

    @field_validator("options")
    @classmethod
    def validate_options(cls, value):
        if len(value) != 4:
            raise ValueError("Fill in the Blank must contain exactly 4 options.")

        if len(set(value)) != 4:
            raise ValueError("Options must be unique.")

        return value


class GuessNumberItem(BaseModel):
    type: Literal["Guess the Number"] = "Guess the Number"
    sport: str
    difficulty: Literal["Easy", "Medium", "Hard"]
    question: str
    target_number: int | float
    tolerance: int | float = Field(gt=0)
    explanation: str
    source_title: str | None = None
    source_url: str | None = None
    grounding_source: str | None = None
