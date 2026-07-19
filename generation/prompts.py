## BUG: guided cloze recognizes each paragraph as 1 question
## => asking for 3 gives 3 paragraphs and 12 blank spaces/questions
## fix later

CATEGORY_INSTRUCTIONS: dict[str, str] = {
    "Reading": (
        "Write a short passage (120-180 words) suitable for upper-intermediate "
        "English learners, followed by comprehension questions. Questions should "
        "test vocabulary-in-context, pronoun/reference resolution, paraphrase "
        "recognition, and overall main idea — similar in style to:\n"
        '  "The word \'obsolete\' in paragraph 2 is OPPOSITE in meaning to ___"\n'
        '  "Which of the following is TRUE according to the passage?"'
    ),
    "Guided Cloze": (
        "Write a short text (80-150 words) on an everyday or school-related topic "
        "with 4-6 numbered blanks. Each blank should test grammar or word choice "
        "in context, e.g. prepositions, verb form, collocations. One question per "
        "blank, four options each, only one grammatically and contextually correct."
    ),
    "Sentence Transformation": (
        "Give one original sentence, then ask which of four options is closest in "
        "meaning or grammatically equivalent — testing reported speech, relative "
        "clauses, comparatives, or passive/active transformation. Distractors should "
        "contain a common learner error (e.g. wrong comparative form, meaning shift), "
        "not just be randomly wrong."
    ),
    "Grammar": (
        "Write a single sentence with one blank testing a specific grammar point "
        "(tense, conditionals, gerunds/infinitives, subject-verb agreement). Four "
        "options, one correct."
    ),
    "Vocabulary": (
        "Write a single sentence with one blank testing word choice — near-synonyms "
        "or collocations where only one word fits the context naturally. Four options."
    ),
    "Phonetics": (
    "Give four words. Three share the same pronunciation for a specified "
    "underlined letter pattern; one differs. Ask which one differs. "
    "Mark the relevant letters in each option using <u>...</u> tags, "
    "consistently applied to all four options."
    ),
    "Stress": (
        "Give four multi-syllable words. Three share the same primary stress "
        "position; one differs. Ask which one differs."
    ),
    "Word Form": (
        "Write a sentence with one blank requiring a word-form change (noun/verb/"
        "adjective/adverb) of a given root word to fit grammatically. Four options, "
        "each a different form of the same root."
    ),
}

JSON_CONTRACT = """
Return ONLY a JSON array, no markdown fences, no commentary before or after.
Each element must match this exact shape:
{
  "category": "<one of the 8 fixed categories>",
  "question_type": "multiple_choice" | "true_false",
  "question_text": "<string>",
  "options": ["<string>", ...] | null,
  "correct_answer": "<string>"
}
Rules:
- multiple_choice: "options" is a list of 4 strings, "correct_answer" must be one of them.
- true_false: "options" is null, "correct_answer" is exactly "true" or "false".
- Do not include explanations, answer keys, or extra fields.
"""

def build_prompt(category: str, count: int) -> str:
    if category not in CATEGORY_INSTRUCTIONS:
        raise ValueError(f"Unknown category: {category}")
    return (
        f"Generate {count} English-practice questions for the category '{category}'.\n\n"
        f"{CATEGORY_INSTRUCTIONS[category]}\n\n"
        f"{JSON_CONTRACT}"
    )