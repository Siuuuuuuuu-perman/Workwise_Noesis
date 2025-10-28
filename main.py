"""
Lightweight FastAPI app for Vercel deployment
Minimal dependencies for serverless function size limits
"""

import os
import json
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Any

# Add backend path to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'app'))

# Import services with graceful fallback
try:
    from services.skills import extract_skills_from_text
    from services.gaps import map_role_to_required_skills, detect_skill_gaps
    from services.ai_analysis import analyze_ai_replacement_risk, get_job_market_analysis
    from services.reflection_agent import get_reflection_agent, ReflectionReport, ReflectionInsight, LearningProgress
    from services.course_recommendations import get_course_service, CourseRecommendation, Course
    from services.assessment import generate_assessment, score_assessment, SOFT_SKILLS_QUESTIONS, INTERVIEW_QUESTIONS
    from services.roadmap import generate_learning_roadmap
    from services.resources import rank_resources_for_skills
    from services.problems import generate_problems_for_skills, get_problem_by_id, validate_solution
    from services.models import AnalyzeRequest, AnalyzeResponse, AssessmentGenerateRequest, AssessmentSubmitRequest, AssessmentResultResponse, RoadmapRequest, RoadmapResponse, ResourcesRequest, ResourcesResponse
    SERVICES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import services: {e}")
    SERVICES_AVAILABLE = False

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
    return {"status": "ok", "environment": os.getenv("ENVIRONMENT", "development"), "services": SERVICES_AVAILABLE}

# Basic skill analysis endpoint
@app.post("/analyze")
async def analyze_resume(request: Dict[str, Any]):
    """Analyze resume and provide skill recommendations"""
    try:
        if not SERVICES_AVAILABLE:
            return {
                "extracted_skills": ["Python", "SQL", "Data Analysis"],
                "skill_gaps": [
                    {
                        "skill": "Machine Learning",
                        "status": "Missing",
                        "recommendation": "Take a machine learning course to enhance your data analysis skills"
                    }
                ],
                "ai_risk": "Low",
                "job_market": "Strong demand for data analysts"
            }
        
        # Extract skills from resume text
        resume_text = request.get("resume_text", "")
        goal = request.get("goal", "Data Analyst")
        
        extracted_skills = extract_skills_from_text(resume_text)
        
        # Map role to required skills
        required_skills = map_role_to_required_skills(goal)
        
        # Detect skill gaps
        skill_gaps = detect_skill_gaps(extracted_skills, required_skills)
        
        # AI replacement risk analysis
        ai_risk = analyze_ai_replacement_risk(goal)
        
        # Job market analysis
        job_market = get_job_market_analysis(goal)
        
        return {
            "extracted_skills": extracted_skills,
            "skill_gaps": skill_gaps,
            "ai_risk": ai_risk,
            "job_market": job_market
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Course recommendations endpoint
@app.post("/courses/recommend")
async def get_course_recommendations(user_profile: Dict[str, Any]):
    """Get AI-powered course recommendations"""
    try:
        if not SERVICES_AVAILABLE:
            return {
                "recommendations": [
                    {
                        "course": {
                            "platform": "Coursera",
                            "title": "Python for Data Science",
                            "description": "Learn Python programming for data analysis",
                            "duration_hours": 40,
                            "rating": 4.5,
                            "price": 49.99
                        },
                        "match_score": 0.9,
                        "reasoning": "Perfect match for your skill gaps"
                    }
                ]
            }
        
        course_service = get_course_service()
        recommendations = course_service.get_ai_course_recommendations(user_profile)
        
        return {"recommendations": recommendations}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Course recommendations failed: {str(e)}")

# Reflection agent endpoint
@app.post("/reflection/generate")
async def generate_reflection_report(user_data: Dict[str, Any]):
    """Generate reflection report using AI"""
    try:
        if not SERVICES_AVAILABLE:
            return {
                "user_id": "demo_user",
                "overall_progress_score": 0.75,
                "key_insights": [
                    {
                        "category": "strength",
                        "title": "Strong Technical Skills",
                        "description": "You have excellent Python and SQL skills",
                        "confidence": 0.9
                    }
                ],
                "recommendations": ["Focus on machine learning", "Practice data visualization"]
            }
        
        reflection_agent = get_reflection_agent()
        report = reflection_agent.create_reflection_report("demo_user", user_data)
        
        return report.dict()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reflection generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)