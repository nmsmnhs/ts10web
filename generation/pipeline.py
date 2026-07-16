from generation.prompts import build_prompt
from generation.gemini_client import call_gemini
from generation.parser import parse_response, ParseResult

def generate_for_category(category: str, count: int) -> ParseResult:
    prompt = build_prompt(category, count)
    raw = call_gemini(prompt)
    return parse_response(raw, category)

def generate_all(categories: list[str], count_per_category: int) -> dict[str, ParseResult]:
    results = {}
    for category in categories:
        try:
            results[category] = generate_for_category(category, count_per_category)
        except Exception as e:
            # network/API failure for this category — log and continue, don't kill the batch
            results[category] = ParseResult(errors=[f"[{category}] Generation failed: {e}"])
    return results

print(generate_for_category("Phonetics", 2))