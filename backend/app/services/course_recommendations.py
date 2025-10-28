"""
Course Recommendation Service - AI-powered course suggestions from multiple learning platforms
Uses NVIDIA Nemotron for intelligent course matching and personalized recommendations
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Course:
    """Data class for course information"""
    platform: str
    course_id: str
    title: str
    description: str
    instructor: str
    duration_hours: int
    difficulty_level: str  # "Beginner", "Intermediate", "Advanced"
    rating: float
    price: float
    currency: str
    url: str
    skills_covered: List[str]
    prerequisites: List[str]
    completion_certificate: bool
    language: str
    enrollment_count: int
    last_updated: datetime

@dataclass
class CourseRecommendation:
    """Data class for course recommendations"""
    course: Course
    match_score: float  # 0.0 to 1.0
    reasoning: str
    priority: str  # "high", "medium", "low"
    estimated_completion_time: int  # days
    learning_path_position: int  # 1, 2, 3, etc.

class CourseRecommendationService:
    """AI-powered course recommendation service using NVIDIA Nemotron"""
    
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_API_KEY")
        self.base_url = os.getenv("NVIDIA_BASE_URL", "https://api.nvcf.nvidia.com/v1")
        self.model = os.getenv("NEMOTRON_MODEL", "nvidia/nemotron-nano-9b-v2")
        
        # Learning platform configurations
        self.platforms = {
            "coursera": {
                "api_base": "https://api.coursera.org/api/courses.v1",
                "search_endpoint": "/search",
                "course_endpoint": "/courses"
            },
            "khan_academy": {
                "api_base": "https://www.khanacademy.org/api/v1",
                "search_endpoint": "/search",
                "course_endpoint": "/courses"
            },
            "udemy": {
                "api_base": "https://www.udemy.com/api-2.0",
                "search_endpoint": "/courses",
                "course_endpoint": "/courses"
            },
            "edx": {
                "api_base": "https://api.edx.org/catalog/v1",
                "search_endpoint": "/courses",
                "course_endpoint": "/courses"
            },
            "linkedin_learning": {
                "api_base": "https://api.linkedin.com/v2",
                "search_endpoint": "/learning",
                "course_endpoint": "/learning"
            }
        }
        
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY environment variable is required")
    
    def _make_ai_request(self, prompt: str, max_tokens: int = 2000) -> str:
        """Make a request to the NVIDIA Nemotron API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system", 
                    "content": "You are an expert course recommendation AI. Provide detailed, personalized course suggestions based on user skills, goals, and learning preferences."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 0.9,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions", 
                headers=headers, 
                json=payload, 
                timeout=30
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            print(f"NVIDIA API Error: {e}")
            raise
        except KeyError:
            print(f"Error parsing AI response: {response.text}")
            raise ValueError("Error parsing AI response")
    
    def search_courses_on_platform(self, platform: str, skill: str, difficulty: str = "Beginner") -> List[Dict[str, Any]]:
        """Search for courses on a specific platform"""
        try:
            platform_config = self.platforms.get(platform)
            if not platform_config:
                return []
            
            # Mock API calls - in production, you'd use real APIs
            mock_courses = self._get_mock_courses(platform, skill, difficulty)
            return mock_courses
            
        except Exception as e:
            print(f"Error searching {platform}: {e}")
            return []
    
    def _get_mock_courses(self, platform: str, skill: str, difficulty: str) -> List[Dict[str, Any]]:
        """Generate mock course data for demonstration"""
        base_courses = {
            "coursera": [
                {
                    "course_id": f"coursera_{skill.lower()}_101",
                    "title": f"{skill} Fundamentals",
                    "description": f"Learn the fundamentals of {skill} with hands-on projects",
                    "instructor": "Dr. Jane Smith",
                    "duration_hours": 40,
                    "difficulty_level": difficulty,
                    "rating": 4.7,
                    "price": 49.0,
                    "currency": "USD",
                    "url": f"https://coursera.org/learn/{skill.lower()}-fundamentals",
                    "skills_covered": [skill, "Problem Solving", "Critical Thinking"],
                    "prerequisites": [],
                    "completion_certificate": True,
                    "language": "English",
                    "enrollment_count": 15000,
                    "last_updated": datetime.now().isoformat()
                },
                {
                    "course_id": f"coursera_{skill.lower()}_advanced",
                    "title": f"Advanced {skill} Techniques",
                    "description": f"Master advanced {skill} concepts and real-world applications",
                    "instructor": "Prof. John Doe",
                    "duration_hours": 60,
                    "difficulty_level": "Advanced",
                    "rating": 4.8,
                    "price": 79.0,
                    "currency": "USD",
                    "url": f"https://coursera.org/learn/{skill.lower()}-advanced",
                    "skills_covered": [skill, "Advanced Techniques", "Project Management"],
                    "prerequisites": [f"{skill} Fundamentals"],
                    "completion_certificate": True,
                    "language": "English",
                    "enrollment_count": 8500,
                    "last_updated": datetime.now().isoformat()
                }
            ],
            "khan_academy": [
                {
                    "course_id": f"khan_{skill.lower()}_basics",
                    "title": f"{skill} Basics",
                    "description": f"Free introduction to {skill} concepts",
                    "instructor": "Khan Academy Team",
                    "duration_hours": 20,
                    "difficulty_level": "Beginner",
                    "rating": 4.5,
                    "price": 0.0,
                    "currency": "USD",
                    "url": f"https://khanacademy.org/computing/{skill.lower()}",
                    "skills_covered": [skill, "Basic Concepts"],
                    "prerequisites": [],
                    "completion_certificate": False,
                    "language": "English",
                    "enrollment_count": 50000,
                    "last_updated": datetime.now().isoformat()
                }
            ],
            "udemy": [
                {
                    "course_id": f"udemy_{skill.lower()}_complete",
                    "title": f"Complete {skill} Bootcamp",
                    "description": f"Comprehensive {skill} course with projects and exercises",
                    "instructor": "Mike Johnson",
                    "duration_hours": 80,
                    "difficulty_level": difficulty,
                    "rating": 4.6,
                    "price": 89.99,
                    "currency": "USD",
                    "url": f"https://udemy.com/course/{skill.lower()}-bootcamp",
                    "skills_covered": [skill, "Practical Applications", "Portfolio Building"],
                    "prerequisites": [],
                    "completion_certificate": True,
                    "language": "English",
                    "enrollment_count": 25000,
                    "last_updated": datetime.now().isoformat()
                }
            ],
            "edx": [
                {
                    "course_id": f"edx_{skill.lower()}_university",
                    "title": f"{skill} from MIT",
                    "description": f"University-level {skill} course from MIT",
                    "instructor": "MIT Faculty",
                    "duration_hours": 100,
                    "difficulty_level": "Advanced",
                    "rating": 4.9,
                    "price": 199.0,
                    "currency": "USD",
                    "url": f"https://edx.org/course/{skill.lower()}-mit",
                    "skills_covered": [skill, "Academic Rigor", "Research Methods"],
                    "prerequisites": ["Mathematics", "Computer Science Basics"],
                    "completion_certificate": True,
                    "language": "English",
                    "enrollment_count": 12000,
                    "last_updated": datetime.now().isoformat()
                }
            ]
        }
        
        return base_courses.get(platform, [])
    
    def get_ai_course_recommendations(self, user_profile: Dict[str, Any]) -> List[CourseRecommendation]:
        """Get AI-powered course recommendations"""
        prompt = f"""
        Based on the user profile below, recommend the best courses for their learning journey.
        Consider their current skills, target role, skill gaps, learning preferences, and budget.
        
        User Profile:
        - Current Skills: {user_profile.get('current_skills', [])}
        - Target Role: {user_profile.get('target_role', 'Unknown')}
        - Skill Gaps: {user_profile.get('skill_gaps', [])}
        - Learning Style: {user_profile.get('learning_style', 'Mixed')}
        - Time Available: {user_profile.get('time_available_hours', 10)} hours/week
        - Budget: ${user_profile.get('budget', 100)}/month
        - Preferred Platforms: {user_profile.get('preferred_platforms', ['Coursera', 'Khan Academy'])}
        - Experience Level: {user_profile.get('experience_level', 'Beginner')}
        
        Return a JSON array of course recommendations with this structure:
        [
            {{
                "platform": "coursera|khan_academy|udemy|edx|linkedin_learning",
                "course_title": "Course Title",
                "match_score": 0.0-1.0,
                "reasoning": "Why this course is recommended",
                "priority": "high|medium|low",
                "estimated_completion_time_days": number,
                "learning_path_position": 1-5,
                "skills_covered": ["skill1", "skill2"],
                "difficulty_level": "Beginner|Intermediate|Advanced",
                "price": number,
                "duration_hours": number
            }}
        ]
        
        Focus on courses that address the most critical skill gaps first.
        """
        
        try:
            response_text = self._make_ai_request(prompt, max_tokens=1500)
            recommendations_data = json.loads(response_text)
            
            recommendations = []
            for rec_data in recommendations_data:
                # Create Course object
                course = Course(
                    platform=rec_data.get("platform", "unknown"),
                    course_id=f"{rec_data.get('platform', 'unknown')}_{rec_data.get('course_title', 'unknown').lower().replace(' ', '_')}",
                    title=rec_data.get("course_title", "Unknown Course"),
                    description=f"AI-recommended course for {user_profile.get('target_role', 'your goals')}",
                    instructor="Various Instructors",
                    duration_hours=rec_data.get("duration_hours", 40),
                    difficulty_level=rec_data.get("difficulty_level", "Intermediate"),
                    rating=4.5,  # Default rating
                    price=rec_data.get("price", 0),
                    currency="USD",
                    url=f"https://{rec_data.get('platform', 'example')}.com/course/{rec_data.get('course_title', 'course').lower().replace(' ', '-')}",
                    skills_covered=rec_data.get("skills_covered", []),
                    prerequisites=[],
                    completion_certificate=True,
                    language="English",
                    enrollment_count=10000,
                    last_updated=datetime.now()
                )
                
                # Create CourseRecommendation object
                recommendation = CourseRecommendation(
                    course=course,
                    match_score=float(rec_data.get("match_score", 0.8)),
                    reasoning=rec_data.get("reasoning", "Recommended based on your profile"),
                    priority=rec_data.get("priority", "medium"),
                    estimated_completion_time=rec_data.get("estimated_completion_time_days", 30),
                    learning_path_position=rec_data.get("learning_path_position", 1)
                )
                
                recommendations.append(recommendation)
            
            return recommendations
            
        except (json.JSONDecodeError, requests.exceptions.RequestException, ValueError) as e:
            print(f"⚠️ NVIDIA API failed, using fallback recommendations: {e}")
            return self._get_fallback_recommendations(user_profile)
    
    def _get_fallback_recommendations(self, user_profile: Dict[str, Any]) -> List[CourseRecommendation]:
        """Fallback recommendations when AI fails"""
        fallback_courses = []
        
        # Get skill gaps
        skill_gaps = user_profile.get('skill_gaps', [])
        if not skill_gaps:
            skill_gaps = ['Python', 'Data Analysis', 'Machine Learning']
        
        # Create fallback recommendations
        for i, skill in enumerate(skill_gaps[:3]):  # Top 3 skills
            course = Course(
                platform="coursera",
                course_id=f"fallback_{skill.lower()}_course",
                title=f"{skill} Fundamentals",
                description=f"Learn {skill} fundamentals with hands-on projects",
                instructor="Expert Instructor",
                duration_hours=40,
                difficulty_level="Beginner",
                rating=4.5,
                price=49.0,
                currency="USD",
                url=f"https://coursera.org/learn/{skill.lower()}-fundamentals",
                skills_covered=[skill],
                prerequisites=[],
                completion_certificate=True,
                language="English",
                enrollment_count=10000,
                last_updated=datetime.now()
            )
            
            recommendation = CourseRecommendation(
                course=course,
                match_score=0.8,
                reasoning=f"Essential {skill} course for your target role",
                priority="high" if i == 0 else "medium",
                estimated_completion_time=30,
                learning_path_position=i + 1
            )
            
            fallback_courses.append(recommendation)
        
        return fallback_courses
    
    def create_learning_path(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive learning path with course recommendations"""
        print(f"🎓 Creating learning path for {user_profile.get('target_role', 'Unknown')} role")
        
        # Get AI recommendations
        recommendations = self.get_ai_course_recommendations(user_profile)
        
        # Organize by priority and learning path position
        recommendations.sort(key=lambda x: (x.priority == "high", x.learning_path_position))
        
        # Calculate total learning time
        total_hours = sum(rec.course.duration_hours for rec in recommendations)
        total_cost = sum(rec.course.price for rec in recommendations)
        
        # Create learning path
        learning_path = {
            "user_profile": user_profile,
            "target_role": user_profile.get('target_role', 'Unknown'),
            "total_courses": len(recommendations),
            "total_hours": total_hours,
            "total_cost": total_cost,
            "estimated_completion_days": max(rec.estimated_completion_time for rec in recommendations) if recommendations else 90,
            "recommendations": [
                {
                    "position": rec.learning_path_position,
                    "platform": rec.course.platform,
                    "title": rec.course.title,
                    "description": rec.course.description,
                    "instructor": rec.course.instructor,
                    "duration_hours": rec.course.duration_hours,
                    "difficulty_level": rec.course.difficulty_level,
                    "rating": rec.course.rating,
                    "price": rec.course.price,
                    "currency": rec.course.currency,
                    "url": rec.course.url,
                    "skills_covered": rec.course.skills_covered,
                    "prerequisites": rec.course.prerequisites,
                    "completion_certificate": rec.course.completion_certificate,
                    "language": rec.course.language,
                    "enrollment_count": rec.course.enrollment_count,
                    "match_score": rec.match_score,
                    "reasoning": rec.reasoning,
                    "priority": rec.priority,
                    "estimated_completion_time_days": rec.estimated_completion_time
                }
                for rec in recommendations
            ],
            "platform_breakdown": self._get_platform_breakdown(recommendations),
            "skill_coverage": self._get_skill_coverage(recommendations),
            "generated_at": datetime.now().isoformat()
        }
        
        print(f"✅ Learning path created with {len(recommendations)} courses")
        return learning_path
    
    def _get_platform_breakdown(self, recommendations: List[CourseRecommendation]) -> Dict[str, int]:
        """Get breakdown of courses by platform"""
        platform_counts = {}
        for rec in recommendations:
            platform = rec.course.platform
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        return platform_counts
    
    def _get_skill_coverage(self, recommendations: List[CourseRecommendation]) -> Dict[str, int]:
        """Get breakdown of skills covered"""
        skill_counts = {}
        for rec in recommendations:
            for skill in rec.course.skills_covered:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
        return skill_counts

# Global instance
_course_service_instance = None

def get_course_service():
    """Get or create course recommendation service instance"""
    global _course_service_instance
    if _course_service_instance is None:
        _course_service_instance = CourseRecommendationService()
    return _course_service_instance
