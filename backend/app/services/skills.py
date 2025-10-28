import re
import os
from typing import List

# Import Nemotron service
try:
    from .nemotron import get_nemotron_service
    NEMOTRON_AVAILABLE = True
except ImportError:
    NEMOTRON_AVAILABLE = False

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
    """Extract skills using Nemotron AI or fallback to rule-based approach"""
    
    # Try Nemotron AI first if available and API key is set
    if NEMOTRON_AVAILABLE and os.getenv("NVIDIA_API_KEY"):
        try:
            nemotron = get_nemotron_service()
            ai_skills = nemotron.extract_skills_from_text(text, user_known_skills)
            if ai_skills:
                print(f"✅ Using Nemotron AI for skill extraction: {len(ai_skills)} skills found")
                return ai_skills
        except Exception as e:
            print(f"⚠️ Nemotron AI failed, falling back to rule-based: {e}")
    
    # Fallback to rule-based extraction
    print("📝 Using rule-based skill extraction")
    text_norm = normalize(text)
    found = set()
    for token in BASIC_SKILL_LEXICON:
        if token in text_norm:
            found.add(token)
    for s in user_known_skills or []:
        if s:
            found.add(normalize(s))
    return sorted(found)


