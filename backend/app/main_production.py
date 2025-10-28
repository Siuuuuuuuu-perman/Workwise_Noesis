import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import xml.etree.ElementTree as ET
import json
import uuid

from .services.skills import extract_skills_from_text
from .services.gaps import map_role_to_required_skills, detect_skill_gaps
from .services.resources import rank_resources_for_skills
from .services.roadmap import generate_learning_roadmap
from .services.assessment import generate_assessment, score_assessment, SOFT_SKILLS_QUESTIONS, INTERVIEW_QUESTIONS
from .services.problems import generate_problems_for_skills, get_problem_by_id, validate_solution
from .services.ai_analysis import analyze_ai_replacement_risk, get_job_market_analysis
from .services.reflection_agent import get_reflection_agent, ReflectionReport, ReflectionInsight, LearningProgress
from .services.models import AnalyzeRequest, AnalyzeResponse, AssessmentGenerateRequest, AssessmentSubmitRequest, AssessmentResultResponse, RoadmapRequest, RoadmapResponse, ResourcesRequest, ResourcesResponse

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
    return {"message": "Noesis API is running", "version": "0.1.0"}

@app.get("/health")
def health() -> dict:
    return {"status": "ok", "environment": os.getenv("ENVIRONMENT", "development")}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    extracted = extract_skills_from_text(
        text=request.resume_text or "",
        user_known_skills=request.known_skills or [],
    )
    required = map_role_to_required_skills(request.goal)
    gaps = detect_skill_gaps(known_skills=extracted, required_skills=required, role=request.goal)
    return AnalyzeResponse(
        extracted_skills=extracted,
        required_skills=required,
        skill_gaps=gaps,
    )


@app.post("/assessment/generate")
async def assessment_generate(request: AssessmentGenerateRequest):
    questions = generate_assessment(
        skills=request.skills,
        num_questions_per_skill=request.num_questions_per_skill or 3,
    )
    return {"questions": questions}


@app.post("/assessment/submit", response_model=AssessmentResultResponse)
async def assessment_submit(request: AssessmentSubmitRequest) -> AssessmentResultResponse:
    result = score_assessment(request.responses)
    return result


@app.post("/resources", response_model=ResourcesResponse)
async def resources(request: ResourcesRequest) -> ResourcesResponse:
    ranked = rank_resources_for_skills(
        missing_skills=request.missing_skills,
        free_preferred=(request.free_preferred if request.free_preferred is not None else True),
        weekly_time_hours=(request.weekly_time_hours if request.weekly_time_hours is not None else 5),
        provider_preferences=request.provider_preferences or [],
    )
    return ResourcesResponse(resources=ranked)


@app.post("/roadmap", response_model=RoadmapResponse)
async def roadmap(request: RoadmapRequest) -> RoadmapResponse:
    plan = generate_learning_roadmap(
        goal=request.goal,
        missing_skills=request.missing_skills,
        weekly_time_hours=request.weekly_time_hours,
        ranked_resources=request.ranked_resources,
        weeks=request.weeks or 6,
    )
    return RoadmapResponse(learning_roadmap=plan)


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload PDF file and convert to XML format for processing"""
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Check file size limit
    max_size = int(os.getenv("MAX_FILE_SIZE_MB", "10")) * 1024 * 1024  # 10MB default
    content = await file.read()
    if len(content) > max_size:
        raise HTTPException(status_code=400, detail=f"File too large. Maximum size: {max_size // (1024*1024)}MB")
    
    try:
        # Convert PDF to text (simplified - in production use proper PDF parsing)
        try:
            from pypdf import PdfReader
            import io
            pdf_reader = PdfReader(io.BytesIO(content))
            text_content = ""
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n"
        except Exception as e:
            # Fallback to PyPDF2
            try:
                import PyPDF2
                import io
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
                text_content = ""
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"
            except Exception:
                raise HTTPException(status_code=400, detail=f"Could not read PDF: {str(e)}")
        
        # Convert text to XML format
        filename = file.filename or "unknown.pdf"
        xml_content = convert_text_to_xml(text_content, filename)
        
        return {
            "filename": filename,
            "xml_content": xml_content,
            "text_content": text_content,
            "message": "PDF successfully converted to XML format"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


def convert_text_to_xml(text: str, filename: str) -> str:
    """Convert extracted text to structured XML format"""
    # Create XML structure
    root = ET.Element("resume")
    root.set("filename", filename)
    
    # Add metadata
    metadata = ET.SubElement(root, "metadata")
    ET.SubElement(metadata, "source").text = "PDF"
    ET.SubElement(metadata, "filename").text = filename
    
    # Add content sections
    content = ET.SubElement(root, "content")
    
    # Split text into sections (basic parsing)
    sections = text.split('\n\n')
    for i, section in enumerate(sections):
        if section.strip():
            section_elem = ET.SubElement(content, "section")
            section_elem.set("id", f"section_{i}")
            section_elem.text = section.strip()
    
    # Add skills section (extracted from text)
    skills_section = ET.SubElement(root, "skills")
    extracted_skills = extract_skills_from_text(text, [])
    for skill in extracted_skills:
        skill_elem = ET.SubElement(skills_section, "skill")
        skill_elem.text = skill
    
    # Convert to string
    return ET.tostring(root, encoding='unicode', method='xml')


@app.post("/analyze-xml")
async def analyze_xml(xml_content: str = Form(...), goal: str = Form(...), weekly_time_hours: int = Form(5)):
    """Analyze skills from XML content"""
    try:
        # Parse XML
        root = ET.fromstring(xml_content)
        
        # Extract text content
        text_content = ""
        for section in root.findall(".//section"):
            if section.text:
                text_content += section.text + "\n"
        
        # Extract skills from XML
        skills_from_xml = []
        for skill in root.findall(".//skill"):
            if skill.text:
                skills_from_xml.append(skill.text)
        
        # Use existing analysis logic
        extracted = extract_skills_from_text(text_content, skills_from_xml)
        required = map_role_to_required_skills(goal)
        gaps = detect_skill_gaps(known_skills=extracted, required_skills=required)
        
        return {
            "xml_parsed": True,
            "extracted_skills": extracted,
            "required_skills": required,
            "skill_gaps": gaps,
            "text_content": text_content[:500] + "..." if len(text_content) > 500 else text_content
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing XML: {str(e)}")


@app.post("/problems/generate")
async def generate_problems(skills: List[str] = Form(...), role: str = Form("data_analyst"), difficulty: str = Form("intermediate")):
    """Generate real-world problems that combine multiple skills"""
    problems = generate_problems_for_skills(skills, role, difficulty)
    return {"problems": problems}


@app.get("/problems/{problem_id}")
async def get_problem(problem_id: str):
    """Get a specific problem by ID"""
    problem = get_problem_by_id(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


@app.post("/problems/{problem_id}/validate")
async def validate_problem_solution(problem_id: str, solution_data: dict):
    """Validate a solution to a problem"""
    result = validate_solution(problem_id, solution_data)
    return result


@app.post("/ai-analysis")
async def ai_replacement_analysis(role: str = Form(...), skills: List[str] = Form(...)):
    """Analyze AI replacement risk for a role and skill set"""
    analysis = analyze_ai_replacement_risk(role, skills)
    return analysis


@app.post("/job-market")
async def job_market_analysis(role: str = Form(...), skills: List[str] = Form(...)):
    """Analyze job market opportunities and likelihood"""
    analysis = get_job_market_analysis(role, skills)
    return analysis


@app.post("/assessment/soft-skills")
async def generate_soft_skills_assessment():
    """Generate soft skills assessment questions"""
    questions = []
    for skill_type, skill_questions in SOFT_SKILLS_QUESTIONS.items():
        for question in skill_questions:
            questions.append({
                "id": str(uuid.uuid4()),
                "skill_type": skill_type,
                "prompt": question["prompt"],
                "options": question["options"],
                "answer_index": question["answer_index"],
                "points": question["points"],
                "explanation": question["explanation"]
            })
    return {"questions": questions}


@app.get("/interview-questions/{role}")
async def get_interview_questions(role: str):
    """Get interview questions for a specific role"""
    role_questions = INTERVIEW_QUESTIONS.get(role.lower(), INTERVIEW_QUESTIONS["data_analyst"])
    return role_questions


@app.get("/roles")
async def get_available_roles():
    """Get list of available STEM roles"""
    roles = [
        {"name": "Data Analyst", "category": "Data Science", "growth_rate": 0.15},
        {"name": "Software Engineer", "category": "Software Development", "growth_rate": 0.22},
        {"name": "Machine Learning Engineer", "category": "AI/ML", "growth_rate": 0.35},
        {"name": "Cybersecurity Analyst", "category": "Security", "growth_rate": 0.28},
        {"name": "Biomedical Engineer", "category": "Healthcare Technology", "growth_rate": 0.12},
        {"name": "Environmental Engineer", "category": "Sustainability", "growth_rate": 0.18}
    ]
    return {"roles": roles}


# =============================================================================
# REFLECTION AGENT ENDPOINTS - AI-Powered Learning Reflection
# =============================================================================

@app.post("/reflection/generate")
async def generate_reflection_report(user_data: dict):
    """Generate comprehensive reflection report using NVIDIA AI"""
    try:
        user_id = user_data.get("user_id", "anonymous")
        reflection_agent = get_reflection_agent()
        
        report = reflection_agent.create_reflection_report(user_id, user_data)
        
        # Convert to JSON-serializable format
        report_dict = {
            "user_id": report.user_id,
            "generated_at": report.generated_at.isoformat(),
            "overall_progress_score": report.overall_progress_score,
            "key_insights": [
                {
                    "category": insight.category,
                    "title": insight.title,
                    "description": insight.description,
                    "confidence": insight.confidence,
                    "actionable": insight.actionable,
                    "priority": insight.priority,
                    "suggested_actions": insight.suggested_actions
                }
                for insight in report.key_insights
            ],
            "learning_progress": [
                {
                    "skill": progress.skill,
                    "current_level": progress.current_level,
                    "target_level": progress.target_level,
                    "progress_percentage": progress.progress_percentage,
                    "time_invested_hours": progress.time_invested_hours,
                    "last_practice_date": progress.last_practice_date.isoformat() if progress.last_practice_date else None,
                    "confidence_score": progress.confidence_score
                }
                for progress in report.learning_progress
            ],
            "recommendations": report.recommendations,
            "next_milestones": report.next_milestones,
            "motivational_message": report.motivational_message
        }
        
        return report_dict
        
    except Exception as e:
        print(f"Error generating reflection report: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate reflection report: {str(e)}")


@app.post("/reflection/insights")
async def get_learning_insights(user_data: dict):
    """Get AI-powered learning insights"""
    try:
        reflection_agent = get_reflection_agent()
        insights = reflection_agent.analyze_learning_patterns(user_data)
        
        insights_dict = [
            {
                "category": insight.category,
                "title": insight.title,
                "description": insight.description,
                "confidence": insight.confidence,
                "actionable": insight.actionable,
                "priority": insight.priority,
                "suggested_actions": insight.suggested_actions
            }
            for insight in insights
        ]
        
        return {"insights": insights_dict}
        
    except Exception as e:
        print(f"Error generating insights: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate insights: {str(e)}")


@app.post("/reflection/progress")
async def analyze_learning_progress(learning_data: List[dict]):
    """Analyze detailed learning progress"""
    try:
        reflection_agent = get_reflection_agent()
        progress_analysis = reflection_agent.generate_progress_analysis(learning_data)
        
        progress_dict = [
            {
                "skill": progress.skill,
                "current_level": progress.current_level,
                "target_level": progress.target_level,
                "progress_percentage": progress.progress_percentage,
                "time_invested_hours": progress.time_invested_hours,
                "last_practice_date": progress.last_practice_date.isoformat() if progress.last_practice_date else None,
                "confidence_score": progress.confidence_score
            }
            for progress in progress_analysis
        ]
        
        return {"progress_analysis": progress_dict}
        
    except Exception as e:
        print(f"Error analyzing progress: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze progress: {str(e)}")


@app.get("/reflection/status")
async def reflection_agent_status():
    """Check reflection agent status and capabilities"""
    try:
        reflection_agent = get_reflection_agent()
        return {
            "status": "active",
            "model": reflection_agent.model,
            "capabilities": [
                "Learning pattern analysis",
                "Progress tracking",
                "SWOT analysis",
                "Personalized recommendations",
                "Motivational guidance",
                "Milestone planning"
            ],
            "ai_powered": True,
            "fallback_mode": True
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "ai_powered": False,
            "fallback_mode": True
        }
