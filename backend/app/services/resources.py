from typing import List, Dict
from .models import ResourceItem


MOCK_PROVIDER_COURSES: List[Dict] = [
    {
        "provider": "Coursera",
        "name": "SQL Basics",
        "link": "https://www.coursera.org/learn/sql-basics",
        "skill": "sql",
        "difficulty": "Beginner",
        "duration_hours": 12,
        "rating": 4.7,
        "price": "Free",
    },
    {
        "provider": "Khan Academy",
        "name": "Statistics & Probability",
        "link": "https://www.khanacademy.org/math/statistics-probability",
        "skill": "statistics",
        "difficulty": "Beginner",
        "duration_hours": 15,
        "rating": 4.8,
        "price": "Free",
    },
    {
        "provider": "Udemy",
        "name": "Tableau A-Z",
        "link": "https://www.udemy.com/course/tableau10/",
        "skill": "tableau",
        "difficulty": "Beginner",
        "duration_hours": 10,
        "rating": 4.5,
        "price": "Paid",
    },
    {
        "provider": "Coursera",
        "name": "Python for Everybody",
        "link": "https://www.coursera.org/specializations/python",
        "skill": "python",
        "difficulty": "Beginner",
        "duration_hours": 30,
        "rating": 4.8,
        "price": "Free",
    },
    {
        "provider": "edX",
        "name": "Data Visualization Basics",
        "link": "https://www.edx.org/learn/data-visualization",
        "skill": "data visualization",
        "difficulty": "Beginner",
        "duration_hours": 8,
        "rating": 4.6,
        "price": "Free",
    },
]


def score_course(
    course: Dict,
    target_skill: str,
    weekly_time_hours: int,
    free_preferred: bool,
    provider_preferences: List[str],
) -> float:
    relevance = 1.0 if course["skill"].lower() == target_skill.lower() else 0.5
    rating = course.get("rating", 0) / 5.0
    duration_match = min(1.0, weekly_time_hours / max(1.0, float(course.get("duration_hours", 1))))
    price_pref = 1.0 if (free_preferred and course.get("price") == "Free") else 0.5
    provider_bonus = 1.1 if (provider_preferences and course.get("provider") in provider_preferences) else 1.0
    score = (relevance * 0.4 + rating * 0.3 + duration_match * 0.2 + price_pref * 0.1) * provider_bonus
    return round(score, 4)


def rank_resources_for_skills(
    missing_skills: List[str],
    weekly_time_hours: int,
    free_preferred: bool,
    provider_preferences: List[str],
) -> List[ResourceItem]:
    ranked: List[ResourceItem] = []
    for skill in missing_skills:
        candidates = [c for c in MOCK_PROVIDER_COURSES if c["skill"].lower() == skill.lower()]
        if not candidates:
            candidates = MOCK_PROVIDER_COURSES  # fallback to all
        scored = [
            {
                **c,
                "score": score_course(c, skill, weekly_time_hours, free_preferred, provider_preferences),
            }
            for c in candidates
        ]
        scored.sort(key=lambda x: x["score"], reverse=True)
        best = scored[0]
        ranked.append(
            ResourceItem(
                provider=best["provider"],
                name=best["name"],
                link=best["link"],
                skill=skill,
                difficulty=best.get("difficulty", "Beginner"),
                duration_hours=best.get("duration_hours", 5),
                rating=best.get("rating", 0.0),
                price=best.get("price", "Free"),
                score=float(best["score"]),
            )
        )
    return ranked



