import re
from typing import List

BASIC_SKILL_LEXICON = {
    "python",
    "excel",
    "sql",
    "tableau",
    "powerbi",
    "statistics",
    "probability",
    "data visualization",
    "epidemiology",
    "pandas",
    "numpy",
    "matplotlib",
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def extract_skills_from_text(text: str, user_known_skills: List[str]) -> List[str]:
    text_norm = normalize(text)
    found = set()
    for token in BASIC_SKILL_LEXICON:
        if token in text_norm:
            found.add(token)
    for s in user_known_skills or []:
        if s:
            found.add(normalize(s))
    return sorted(found)


