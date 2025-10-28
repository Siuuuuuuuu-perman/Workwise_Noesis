from typing import List, Dict
from .models import ResourceItem


PROBLEM_BANK: Dict[str, List[Dict]] = {
    "data_analyst": [
        {
            "id": "da_001",
            "title": "E-commerce Sales Analysis",
            "description": "Analyze sales data to identify trends and optimize marketing spend",
            "skills_required": ["python", "pandas", "sql", "data visualization"],
            "difficulty": "intermediate",
            "points": 150,
            "scenario": "You're a data analyst at an e-commerce company. The marketing team wants to understand which products are driving the most revenue and which customer segments are most valuable.",
            "data_provided": "Sales transactions, customer demographics, product catalog, marketing campaigns",
            "deliverables": [
                "Top 10 products by revenue",
                "Customer segmentation analysis", 
                "Marketing ROI by channel",
                "Interactive dashboard"
            ],
            "hints": [
                "Start by cleaning and exploring the sales data",
                "Use pandas for data manipulation and aggregation",
                "Create visualizations to identify patterns",
                "Consider seasonality in your analysis"
            ]
        },
        {
            "id": "da_002", 
            "title": "A/B Test Analysis",
            "description": "Analyze A/B test results to determine if a new feature should be launched",
            "skills_required": ["statistics", "python", "pandas"],
            "difficulty": "intermediate",
            "points": 120,
            "scenario": "Your product team ran an A/B test on a new checkout flow. You need to determine if the new flow significantly improves conversion rates.",
            "data_provided": "User behavior data, conversion events, test group assignments",
            "deliverables": [
                "Statistical significance test",
                "Conversion rate comparison",
                "Confidence intervals",
                "Recommendation with reasoning"
            ],
            "hints": [
                "Use appropriate statistical tests (t-test, chi-square)",
                "Check for statistical significance (p < 0.05)",
                "Consider practical significance (effect size)",
                "Account for multiple testing if needed"
            ]
        }
    ],
    "health_data_analyst": [
        {
            "id": "hda_001",
            "title": "Patient Readmission Prediction",
            "description": "Build a model to predict which patients are likely to be readmitted",
            "skills_required": ["python", "pandas", "statistics", "epidemiology"],
            "difficulty": "advanced",
            "points": 200,
            "scenario": "A hospital wants to reduce readmission rates. You need to identify patients at high risk of readmission within 30 days.",
            "data_provided": "Patient demographics, medical history, treatment details, readmission status",
            "deliverables": [
                "Risk prediction model",
                "Feature importance analysis",
                "Model validation results",
                "Clinical recommendations"
            ],
            "hints": [
                "Consider both clinical and demographic factors",
                "Use appropriate ML algorithms (logistic regression, random forest)",
                "Validate your model properly",
                "Consider ethical implications of predictions"
            ]
        }
    ]
}


def generate_problems_for_skills(skills: List[str], role: str = "data_analyst", difficulty: str = "intermediate") -> List[Dict]:
    """Generate real-world problems that combine multiple skills"""
    role_problems = PROBLEM_BANK.get(role.lower(), PROBLEM_BANK["data_analyst"])
    
    # Filter problems that use the available skills
    relevant_problems = []
    for problem in role_problems:
        required_skills = [s.lower() for s in problem["skills_required"]]
        if any(skill.lower() in required_skills for skill in skills):
            if problem["difficulty"] == difficulty:
                relevant_problems.append(problem)
    
    return relevant_problems[:3]  # Return top 3 problems


def get_problem_by_id(problem_id: str) -> Dict:
    """Get a specific problem by ID"""
    for role, problems in PROBLEM_BANK.items():
        for problem in problems:
            if problem["id"] == problem_id:
                return problem
    return {}


def validate_solution(problem_id: str, solution_data: Dict) -> Dict:
    """Validate a solution to a problem"""
    problem = get_problem_by_id(problem_id)
    if not problem:
        return {"valid": False, "message": "Problem not found"}
    
    # Basic validation logic (in production, this would be more sophisticated)
    score = 0
    feedback = []
    
    # Check if all deliverables are addressed
    deliverables = problem.get("deliverables", [])
    provided_deliverables = solution_data.get("deliverables", [])
    
    for deliverable in deliverables:
        if any(deliverable.lower() in str(provided).lower() for provided in provided_deliverables):
            score += 20
            feedback.append(f"✅ {deliverable} addressed")
        else:
            feedback.append(f"❌ {deliverable} missing")
    
    # Check code quality indicators
    if solution_data.get("code_provided"):
        score += 30
        feedback.append("✅ Code solution provided")
    
    if solution_data.get("visualizations"):
        score += 20
        feedback.append("✅ Visualizations included")
    
    if solution_data.get("statistical_analysis"):
        score += 20
        feedback.append("✅ Statistical analysis performed")
    
    # Calculate mastery points earned
    mastery_points = int(score * problem.get("points", 100) / 100)
    
    return {
        "valid": score >= 60,
        "score": score,
        "mastery_points": mastery_points,
        "feedback": feedback,
        "next_steps": [
            "Review the feedback and improve your solution",
            "Try a more advanced problem",
            "Focus on the missing deliverables"
        ] if score < 80 else [
            "Excellent work! Try a more challenging problem",
            "Consider documenting your approach",
            "Share your solution with the community"
        ]
    }
