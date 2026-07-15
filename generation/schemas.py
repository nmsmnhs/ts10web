# generation/schemas.py
from typing import Literal
from pydantic import BaseModel, Field, model_validator

Category = Literal[
    "Grammar", "Vocabulary", "Phonetics", "Stress",
    "Reading", "Guided Cloze", "Sentence Transformation", "Word Form",
]

class QuestionCandidate(BaseModel):
    category: Category
    question_type: Literal["multiple_choice", "true_false"]
    question_text: str = Field(min_length=1)
    options: list[str] | None = None
    correct_answer: str = Field(min_length=1)

    @model_validator(mode="after")
    def check_options_match_type(self):
        if self.question_type == "multiple_choice":
            if not self.options or len(self.options) < 2:
                raise ValueError("multiple_choice requires at least 2 options")
            if self.correct_answer not in self.options:
                raise ValueError("correct_answer must be one of options")
        else:
            if self.options is not None:
                raise ValueError("true_false must not have options")
            if self.correct_answer.lower() not in {"true", "false"}:
                raise ValueError("true_false correct_answer must be 'true' or 'false'")
        return self