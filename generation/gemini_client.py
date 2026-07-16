import os
from google import genai

_client: genai.Client | None = None

_client: genai.Client | None = None

def _get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "No Gemini API key found. Set GEMINI_API_KEY (or API_KEY) in .env"
            )
        _client = genai.Client(api_key=api_key)
    return _client

def call_gemini(prompt: str, model: str = "gemini-2.5-flash") -> str:
    """Send a prompt, return raw response text. Raises on API failure — caller decides retry policy."""
    response = _get_client().models.generate_content(model=model, contents=prompt)
    return response.text