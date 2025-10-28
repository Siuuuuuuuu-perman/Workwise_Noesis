from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class AnalyzeRequest(BaseModel):
    name: Optional[str] = None
    goal: str
    known_skills: Optional[List[str]] = []
    weekly_time_hours: Optional[int] = 5
    resume_text: Optional[str] = ""


class SkillGap(BaseModel):
    skill: str
    status: str  # Known, Missing, Partial
    proficiency_level: str  # Beginner, Intermediate, Advanced, Expert
    required_proficiency: str  # What level is needed for the role
    current_score: float  # 0.0 to 1.0
    required_score: float  # 0.0 to 1.0
    reasoning: str  # Why this skill is needed at this level
    recommendation: Optional[str] = None
    mastery_points: int = 0  # Points needed to master this skill


class AnalyzeResponse(BaseModel):
    extracted_skills: List[str]
    required_skills: List[str]
    skill_gaps: List[SkillGap]


class AssessmentQuestion(BaseModel):
    id: str
    skill: str
    prompt: str
    options: List[str]
    answer_index: int


class AssessmentGenerateRequest(BaseModel):
    skills: List[str]
    num_questions_per_skill: Optional[int] = 3


class AssessmentSubmitRequest(BaseModel):
    responses: List[Dict[str, Any]]  # each: {id, selected_index}


class AssessmentResult(BaseModel):
    skill: str
    correct: int
    total: int
    score: float
    status: str  # Known / Partial / Missing


class AssessmentResultResponse(BaseModel):
    results: List[AssessmentResult]
    updated_known_skills: List[str]


class ResourceItem(BaseModel):
    provider: str
    name: str
    link: str
    skill: str
    difficulty: str
    duration_hours: int
    rating: float
    price: str  # Free/Paid
    score: float


class ResourcesRequest(BaseModel):
    missing_skills: List[str]
    weekly_time_hours: Optional[int] = 5
    free_preferred: Optional[bool] = True
    provider_preferences: Optional[List[str]] = []


class ResourcesResponse(BaseModel):
    resources: List[ResourceItem]


class RoadmapRequest(BaseModel):
    goal: str
    missing_skills: List[str]
    weekly_time_hours: int
    ranked_resources: List[ResourceItem]
    weeks: Optional[int] = 6


class RoadmapEntry(BaseModel):
    week: int
    topic: str
    resource: str
    goal: str
    hours: int


class RoadmapResponse(BaseModel):
    learning_roadmap: List[RoadmapEntry]


