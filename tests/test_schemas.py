# tests/test_schemas.py
import pytest
from pydantic import ValidationError
from generation.schemas import QuestionCandidate

def test_valid_multiple_choice():
    q = QuestionCandidate(
        category="Grammar", question_type="multiple_choice",
        question_text="Which word is a verb?",
        options=["run", "blue", "quickly", "table"], correct_answer="run",
    )
    assert q.correct_answer in q.options

def test_valid_true_false():
    q = QuestionCandidate(
        category="Phonetics", question_type="true_false",
        question_text="'Ph' is always pronounced /f/.", correct_answer="false",
    )
    assert q.options is None

@pytest.mark.parametrize("bad_payload", [
    dict(category="Grammar", question_type="multiple_choice",
         question_text="x", options=None, correct_answer="run"),          # MC missing options
    dict(category="Grammar", question_type="true_false",
         question_text="x", options=["a", "b"], correct_answer="true"),   # TF with options
    dict(category="Grammar", question_type="multiple_choice",
         question_text="x", options=["a", "b"], correct_answer="c"),      # answer not in options
    dict(category="Spelling", question_type="true_false",
         question_text="x", correct_answer="true"),                       # unknown category
])
def test_junk_llm_output_rejected(bad_payload):
    with pytest.raises(ValidationError):
        QuestionCandidate(**bad_payload)