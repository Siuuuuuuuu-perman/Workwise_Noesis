import uuid
from typing import List, Dict
from .models import AssessmentQuestion, AssessmentResult, AssessmentResultResponse


SOFT_SKILLS_QUESTIONS: Dict[str, List[Dict]] = {
    "communication": [
        {
            "prompt": "How would you explain a complex technical concept to a non-technical stakeholder?",
            "options": [
                "Use technical jargon to show expertise",
                "Create analogies and visual aids",
                "Send them a technical document",
                "Avoid explaining complex topics"
            ],
            "answer_index": 1,
            "points": 15,
            "explanation": "Effective communication requires simplifying complex concepts using analogies and visual aids."
        },
        {
            "prompt": "What's the best approach when presenting data analysis results to executives?",
            "options": [
                "Show all raw data and technical details",
                "Focus on business impact and actionable insights",
                "Use only technical terminology",
                "Present findings without context"
            ],
            "answer_index": 1,
            "points": 20,
            "explanation": "Executive presentations should focus on business impact and actionable insights, not technical details."
        }
    ],
    "leadership": [
        {
            "prompt": "How would you handle a team member who consistently misses deadlines?",
            "options": [
                "Publicly criticize them in team meetings",
                "Ignore the problem and hope it improves",
                "Have a private conversation to understand challenges",
                "Immediately replace them"
            ],
            "answer_index": 2,
            "points": 25,
            "explanation": "Effective leadership involves understanding team challenges and providing support through private conversations."
        }
    ],
    "problem_solving": [
        {
            "prompt": "When facing an unexpected technical challenge, what's your first step?",
            "options": [
                "Panic and ask for help immediately",
                "Research the problem and break it into smaller parts",
                "Ignore the problem and move on",
                "Blame external factors"
            ],
            "answer_index": 1,
            "points": 20,
            "explanation": "Effective problem-solving involves systematic analysis and breaking complex problems into manageable parts."
        }
    ],
    "adaptability": [
        {
            "prompt": "How do you handle learning a new technology that's completely different from your expertise?",
            "options": [
                "Avoid it and stick to familiar tools",
                "Complain about having to learn new things",
                "Embrace the challenge and create a learning plan",
                "Delegate the task to someone else"
            ],
            "answer_index": 2,
            "points": 15,
            "explanation": "Adaptability is crucial in tech careers - embracing new challenges and creating learning plans shows growth mindset."
        }
    ]
}

INTERVIEW_QUESTIONS: Dict[str, Dict[str, List[Dict]]] = {
    "data_analyst": {
        "technical": [
            {
                "question": "How would you handle missing data in a dataset?",
                "category": "Data Cleaning",
                "difficulty": "Intermediate",
                "sample_answer": "First, I'd analyze the pattern of missingness (MCAR, MAR, or MNAR). Then I'd choose appropriate imputation methods like mean/median for numerical data, mode for categorical, or advanced methods like KNN imputation. I'd also consider if the missing data is informative and document my approach.",
                "follow_up": "What if 50% of your dataset is missing?",
                "key_points": ["Pattern analysis", "Appropriate imputation", "Documentation", "Business impact"]
            },
            {
                "question": "Explain the difference between correlation and causation.",
                "category": "Statistics",
                "difficulty": "Beginner",
                "sample_answer": "Correlation measures the strength of a linear relationship between variables, while causation implies that one variable directly influences another. Correlation doesn't imply causation - there could be confounding variables or reverse causality.",
                "follow_up": "Give an example where correlation doesn't imply causation.",
                "key_points": ["Definition difference", "Confounding variables", "Examples", "Experimental design"]
            }
        ],
        "behavioral": [
            {
                "question": "Tell me about a time you had to present complex data to non-technical stakeholders.",
                "category": "Communication",
                "difficulty": "Intermediate",
                "sample_answer": "I was presenting sales analysis to marketing executives. I created visual dashboards, used business language instead of technical terms, focused on actionable insights, and prepared for questions about methodology. The result was increased budget allocation for our recommendations.",
                "follow_up": "How did you handle pushback on your recommendations?",
                "key_points": ["STAR method", "Business impact", "Visualization", "Stakeholder management"]
            }
        ]
    },
    "software_engineer": {
        "technical": [
            {
                "question": "How would you design a URL shortener like bit.ly?",
                "category": "System Design",
                "difficulty": "Advanced",
                "sample_answer": "I'd consider: 1) Hash function for URL encoding, 2) Database schema for URL storage, 3) Caching strategy for popular URLs, 4) Load balancing for high traffic, 5) Analytics for click tracking, 6) Security considerations.",
                "follow_up": "How would you handle 1 billion URLs?",
                "key_points": ["Scalability", "Database design", "Caching", "Load balancing", "Security"]
            }
        ],
        "behavioral": [
            {
                "question": "Describe a challenging bug you had to debug.",
                "category": "Problem Solving",
                "difficulty": "Intermediate",
                "sample_answer": "I encountered a memory leak in a production system. I used systematic debugging: reproduced the issue, used profiling tools, identified the root cause in a recursive function, implemented a fix with proper testing, and monitored the solution.",
                "follow_up": "How did you prevent similar issues in the future?",
                "key_points": ["Systematic approach", "Tools used", "Root cause analysis", "Prevention measures"]
            }
        ]
    }
}

QUESTION_BANK: Dict[str, Dict[str, List[Dict]]] = {
    "python": {
        "beginner": [
            {
                "prompt": "Which data structure preserves insertion order and allows duplicates?",
                "options": ["set", "list", "dict", "tuple"],
                "answer_index": 1,
                "points": 10,
                "explanation": "Lists preserve insertion order and allow duplicate elements."
            },
            {
                "prompt": "What does len({'a':1,'b':2}) return?",
                "options": ["1", "2", "3", "Error"],
                "answer_index": 1,
                "points": 10,
                "explanation": "len() returns the number of key-value pairs in a dictionary."
            }
        ],
        "intermediate": [
            {
                "prompt": "What is the output of [x**2 for x in range(5) if x%2==0]?",
                "options": ["[0, 4, 16]", "[1, 9, 25]", "[0, 1, 4, 9, 16]", "[0, 4]"],
                "answer_index": 3,
                "points": 20,
                "explanation": "List comprehension with condition: even numbers (0,2,4) squared = [0, 4, 16]"
            },
            {
                "prompt": "Which method is used to add an element to the end of a list?",
                "options": ["append()", "insert()", "extend()", "add()"],
                "answer_index": 0,
                "points": 15,
                "explanation": "append() adds a single element to the end of the list."
            }
        ],
        "advanced": [
            {
                "prompt": "What does this code return: lambda x: x*2 if x>0 else 0?",
                "options": ["Doubles positive numbers, 0 for negative", "Always returns 0", "Syntax error", "Returns x*2"],
                "answer_index": 0,
                "points": 30,
                "explanation": "Lambda function that doubles positive numbers, returns 0 for non-positive numbers."
            }
        ]
    },
    "sql": [
        {
            "prompt": "Which SQL clause filters rows before grouping?",
            "options": ["WHERE", "HAVING", "GROUP BY", "ORDER BY"],
            "answer_index": 0,
        },
        {
            "prompt": "What does SELECT COUNT(*) FROM t return?",
            "options": ["Sum of values", "Number of rows", "Number of columns", "Distinct rows"],
            "answer_index": 1,
        },
    ],
    "statistics": [
        {
            "prompt": "Mean of [2, 4, 6] is:",
            "options": ["3", "4", "5", "6"],
            "answer_index": 1,
        },
        {
            "prompt": "Probability values lie in range:",
            "options": ["(-inf, inf)", "[0,1]", "[0,inf)", "(-1,1)"],
            "answer_index": 1,
        },
    ],
}


def generate_assessment(skills: List[str], num_questions_per_skill: int = 3) -> List[AssessmentQuestion]:
    questions: List[AssessmentQuestion] = []
    for skill in skills:
        skill_bank = QUESTION_BANK.get(skill.lower(), {})
        if isinstance(skill_bank, dict):
            # New format with difficulty levels
            for difficulty in ["beginner", "intermediate", "advanced"]:
                level_questions = skill_bank.get(difficulty, [])
                chosen = level_questions[:max(1, num_questions_per_skill // 3)]
                for item in chosen:
                    questions.append(
                        AssessmentQuestion(
                            id=str(uuid.uuid4()),
                            skill=skill,
                            prompt=f"[{difficulty.upper()}] {item['prompt']}",
                            options=item["options"],
                            answer_index=item["answer_index"],
                        )
                    )
        else:
            # Legacy format
            chosen = skill_bank[: num_questions_per_skill]
            for item in chosen:
                questions.append(
                    AssessmentQuestion(
                        id=str(uuid.uuid4()),
                        skill=skill,
                        prompt=item["prompt"],
                        options=item["options"],
                        answer_index=item["answer_index"],
                    )
                )
    return questions


def score_assessment(responses: List[Dict]) -> AssessmentResultResponse:
    # responses: [{id, skill, selected_index, answer_index}]
    skill_to_counts: Dict[str, Dict[str, int]] = {}
    updated_known_skills: List[str] = []
    for r in responses:
        skill = r.get("skill")
        correct = 1 if r.get("selected_index") == r.get("answer_index") else 0
        if skill not in skill_to_counts:
            skill_to_counts[skill] = {"correct": 0, "total": 0}
        skill_to_counts[skill]["correct"] += correct
        skill_to_counts[skill]["total"] += 1

    results: List[AssessmentResult] = []
    for skill, counts in skill_to_counts.items():
        total = max(1, counts["total"])  # avoid div by zero
        score = counts["correct"] / total
        status = "Known" if score >= 0.8 else ("Partial" if score >= 0.5 else "Missing")
        if status == "Known":
            updated_known_skills.append(skill)
        results.append(
            AssessmentResult(
                skill=skill,
                correct=counts["correct"],
                total=total,
                score=round(score, 2),
                status=status,
            )
        )
    return AssessmentResultResponse(results=results, updated_known_skills=sorted(updated_known_skills))




