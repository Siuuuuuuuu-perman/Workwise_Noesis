"""
Lightweight FastAPI app for Vercel deployment
Minimal dependencies for serverless function size limits
"""

import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Any

# Production configuration
app = FastAPI(
    title="Noesis API", 
    version="0.1.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,
    redoc_url="/redoc" if os.getenv("ENVIRONMENT") != "production" else None
)

# Production CORS configuration
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8501").split(",")
if os.getenv("ENVIRONMENT") == "production":
    allowed_origins = [origin.strip() for origin in allowed_origins if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc) if os.getenv("ENVIRONMENT") != "production" else "Something went wrong"}
    )

@app.get("/")
def root():
    return {"message": "WorkWise Noesis API - AI-Powered Learning Platform", "status": "active"}

@app.get("/health")
def health() -> dict:
    return {"status": "ok", "environment": os.getenv("ENVIRONMENT", "development")}

# Basic skill analysis endpoint
@app.post("/analyze")
async def analyze_skills(request: Dict[str, Any]):
    """Basic skill analysis with lightweight implementation"""
    try:
        goal = request.get("goal", "Data Analyst")
        known_skills = request.get("known_skills", [])
        resume_text = request.get("resume_text", "")
        
        # Simple skill extraction (lightweight)
        extracted_skills = []
        if resume_text:
            text_lower = resume_text.lower()
            common_skills = ["python", "sql", "excel", "javascript", "java", "c++", "machine learning", "data analysis", "statistics"]
            for skill in common_skills:
                if skill in text_lower:
                    extracted_skills.append(skill)
        
        # Add known skills
        extracted_skills.extend([skill.lower() for skill in known_skills if skill])
        extracted_skills = list(set(extracted_skills))  # Remove duplicates
        
        # Basic role requirements
        role_requirements = {
            "data_analyst": ["statistics", "python", "sql", "excel", "data visualization"],
            "software_engineer": ["programming", "algorithms", "system design", "databases"],
            "data_scientist": ["python", "machine learning", "statistics", "sql", "data analysis"],
            "machine_learning_engineer": ["python", "machine learning", "deep learning", "statistics", "tensorflow"]
        }
        
        required_skills = role_requirements.get(goal.lower().replace(" ", "_"), ["python", "sql", "statistics"])
        
        # Generate skill gaps
        skill_gaps = []
        for skill in required_skills:
            status = "Known" if skill in extracted_skills else "Missing"
            skill_gaps.append({
                "skill": skill,
                "status": status,
                "proficiency_level": "Intermediate" if status == "Known" else "Beginner",
                "required_proficiency": "Advanced",
                "current_score": 0.8 if status == "Known" else 0.2,
                "required_score": 0.8,
                "reasoning": f"Essential skill for {goal} role",
                "recommendation": f"Start with {skill} fundamentals",
                "mastery_points": 150
            })
        
        return {
            "extracted_skills": extracted_skills,
            "required_skills": required_skills,
            "skill_gaps": skill_gaps
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Basic course recommendations
@app.post("/courses/recommend")
async def get_course_recommendations(user_profile: Dict[str, Any]):
    """Basic course recommendations"""
    try:
        target_role = user_profile.get("target_role", "Data Analyst")
        skill_gaps = user_profile.get("skill_gaps", [])
        
        # Extract skills from gaps
        skills = []
        for gap in skill_gaps:
            if isinstance(gap, dict):
                skills.append(gap.get("skill", "Unknown"))
            else:
                skills.append(str(gap))
        
        if not skills:
            skills = ["Python", "SQL", "Statistics"]
        
        # Generate basic recommendations
        recommendations = []
        platforms = ["Coursera", "Khan Academy", "Udemy"]
        
        for i, skill in enumerate(skills[:3]):
            platform = platforms[i % len(platforms)]
            recommendations.append({
                "position": i + 1,
                "platform": platform.lower().replace(" ", "_"),
                "title": f"{skill} Fundamentals",
                "description": f"Learn {skill} fundamentals for {target_role}",
                "instructor": "Expert Instructor",
                "duration_hours": 40,
                "difficulty_level": "Beginner",
                "rating": 4.5,
                "price": 49.0 if platform != "Khan Academy" else 0.0,
                "currency": "USD",
                "url": f"https://{platform.lower().replace(' ', '')}.com/learn/{skill.lower()}-fundamentals",
                "skills_covered": [skill],
                "prerequisites": [],
                "completion_certificate": True,
                "language": "English",
                "enrollment_count": 10000,
                "match_score": 0.8,
                "reasoning": f"Essential {skill} course for {target_role}",
                "priority": "high" if i == 0 else "medium",
                "estimated_completion_time_days": 30
            })
        
        return {"recommendations": recommendations}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Course recommendations failed: {str(e)}")

# Basic reflection insights
@app.post("/reflection/insights")
async def get_learning_insights(user_data: Dict[str, Any]):
    """Basic learning insights"""
    try:
        insights = [
            {
                "category": "opportunity",
                "title": "Consistent Practice",
                "description": "Regular practice sessions will accelerate your learning progress",
                "confidence": 0.8,
                "actionable": True,
                "priority": "high",
                "suggested_actions": ["Schedule daily practice sessions", "Set specific learning goals"]
            },
            {
                "category": "strength",
                "title": "Learning Commitment",
                "description": "Your dedication to skill development is commendable",
                "confidence": 0.9,
                "actionable": False,
                "priority": "medium",
                "suggested_actions": ["Maintain current learning pace"]
            }
        ]
        
        return {"insights": insights}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insights generation failed: {str(e)}")

# Service status endpoints
@app.get("/courses/status")
async def course_service_status():
    return {
        "status": "active",
        "model": "lightweight",
        "supported_platforms": ["coursera", "khan_academy", "udemy"],
        "capabilities": [
            "Basic course recommendations",
            "Skill-based matching",
            "Learning insights"
        ],
        "ai_powered": False,
        "fallback_mode": True
    }

@app.get("/reflection/status")
async def reflection_agent_status():
    return {
        "status": "active",
        "model": "lightweight",
        "capabilities": [
            "Basic learning insights",
            "Progress tracking",
            "Motivational guidance"
        ],
        "ai_powered": False,
        "fallback_mode": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
