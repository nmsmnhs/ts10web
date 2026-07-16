import json
from dataclasses import dataclass, field
from pydantic import ValidationError
from generation.schemas import QuestionCandidate

@dataclass
class ParseResult:
    candidates: list[QuestionCandidate] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def _strip_markdown_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        text = text.rsplit("```", 1)[0]
    return text.strip()

def parse_response(raw_text: str, category: str) -> ParseResult:
    result = ParseResult()
    cleaned = _strip_markdown_fences(raw_text)

    try:
        items = json.loads(cleaned)
    except json.JSONDecodeError as e:
        result.errors.append(f"[{category}] Response was not valid JSON: {e}")
        return result  # nothing to validate, but we RETURN — not raise, not break outer loop

    if not isinstance(items, list):
        result.errors.append(f"[{category}] Expected a JSON array, got {type(items).__name__}")
        return result

    for i, item in enumerate(items):
        try:
            result.candidates.append(QuestionCandidate(**item))
        except ValidationError as e:
            result.errors.append(f"[{category}] Item {i} failed validation: {e}")
            # deliberately no break — one bad item doesn't discard the rest

    return result