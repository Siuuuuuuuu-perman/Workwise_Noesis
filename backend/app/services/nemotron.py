import os
import requests
import json
from typing import List, Dict, Any, Optional
from .models import SkillGap

class NemotronService:
    """Service for integrating with NVIDIA Nemotron Nano v12 model"""
    
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_API_KEY")
        self.base_url = os.getenv("NVIDIA_BASE_URL", "https://api.nvcf.nvidia.com/v1")
        self.model = os.getenv("NEMOTRON_MODEL", "nvidia/nemotron-nano-9b-v2")
        
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY environment variable is required")
    
    def _make_request(self, prompt: str, max_tokens: int = 1000) -> str:
        """Make a request to the Nemotron API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": 0.3,
            "top_p": 0.9
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            print(f"NVIDIA API Error: {e}")
            return ""
        except (KeyError, IndexError) as e:
            print(f"Response parsing error: {e}")
            return ""
    
    def extract_skills_from_text(self, text: str, user_known_skills: List[str] = None) -> List[str]:
        """Extract skills from text using Nemotron Nano v12"""
        
        prompt = f"""
        Analyze the following text and extract all technical skills, programming languages, tools, frameworks, and competencies mentioned. 
        Focus on skills relevant to STEM careers (Data Science, Software Engineering, AI/ML, etc.).
        
        Text: "{text}"
        
        Known skills from user: {user_known_skills or []}
        
        Return ONLY a JSON array of skill names, normalized to lowercase. 
        Example: ["python", "sql", "machine learning", "pandas", "tensorflow"]
        
        Skills to look for:
        - Programming languages (Python, R, Java, JavaScript, etc.)
        - Data analysis tools (Pandas, NumPy, SQL, Excel, etc.)
        - Machine Learning frameworks (TensorFlow, PyTorch, Scikit-learn, etc.)
        - Visualization tools (Tableau, PowerBI, Matplotlib, etc.)
        - Cloud platforms (AWS, Azure, GCP, etc.)
        - Databases (MySQL, PostgreSQL, MongoDB, etc.)
        - Software tools (Git, Docker, Kubernetes, etc.)
        - Domain knowledge (Statistics, Mathematics, etc.)
        """
        
        response = self._make_request(prompt, max_tokens=500)
        
        try:
            # Try to parse JSON response
            skills = json.loads(response)
            if isinstance(skills, list):
                return [skill.lower().strip() for skill in skills if skill.strip()]
        except json.JSONDecodeError:
            # Fallback: extract skills from text response
            skills = []
            lines = response.split('\n')
            for line in lines:
                if line.strip().startswith('"') and line.strip().endswith('"'):
                    skill = line.strip().strip('"').lower()
                    if skill:
                        skills.append(skill)
        
        # Combine with user-provided skills
        if user_known_skills:
            skills.extend([skill.lower().strip() for skill in user_known_skills])
        
        return list(set(skills))  # Remove duplicates
    
    def analyze_skill_gaps_with_ai(self, known_skills: List[str], target_role: str) -> List[SkillGap]:
        """Analyze skill gaps using AI-powered analysis"""
        
        prompt = f"""
        Analyze the skill gaps for someone transitioning to a {target_role} role.
        
        Current skills: {known_skills}
        Target role: {target_role}
        
        For each missing skill, provide:
        1. Skill name
        2. Current proficiency level (Beginner/Intermediate/Advanced/Expert)
        3. Required proficiency level for the role
        4. Current score (0.0-1.0)
        5. Required score (0.0-1.0)
        6. Reasoning why this skill is important
        7. Specific learning recommendation
        8. Mastery points needed (50-200)
        
        Return a JSON array with this structure:
        [
            {{
                "skill": "skill_name",
                "status": "Missing|Partial|Known",
                "proficiency_level": "Beginner",
                "required_proficiency": "Intermediate",
                "current_score": 0.2,
                "required_score": 0.7,
                "reasoning": "Why this skill matters",
                "recommendation": "Specific learning path",
                "mastery_points": 150
            }}
        ]
        """
        
        response = self._make_request(prompt, max_tokens=1500)
        
        try:
            gaps_data = json.loads(response)
            if isinstance(gaps_data, list):
                return [SkillGap(**gap) for gap in gaps_data]
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            print(f"Error parsing AI response: {e}")
        
        # Fallback to basic gap analysis
        return self._fallback_gap_analysis(known_skills, target_role)
    
    def generate_assessment_questions(self, skills: List[str], num_questions: int = 3) -> List[Dict[str, Any]]:
        """Generate assessment questions using AI"""
        
        prompt = f"""
        Generate {num_questions} assessment questions for each of these skills: {skills}
        
        For each question, provide:
        1. A clear, practical question
        2. 4 multiple choice options
        3. The correct answer index (0-3)
        4. Difficulty level (Beginner/Intermediate/Advanced)
        5. Brief explanation of the correct answer
        
        Return JSON format:
        [
            {{
                "id": "unique_id",
                "skill": "skill_name",
                "prompt": "Question text",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "answer_index": 1,
                "difficulty": "Intermediate",
                "explanation": "Why this answer is correct"
            }}
        ]
        """
        
        response = self._make_request(prompt, max_tokens=2000)
        
        try:
            questions = json.loads(response)
            if isinstance(questions, list):
                # Add unique IDs if missing
                for i, q in enumerate(questions):
                    if "id" not in q:
                        q["id"] = f"nemotron_q_{i}_{hash(q.get('prompt', ''))}"
                return questions
        except json.JSONDecodeError as e:
            print(f"Error parsing assessment questions: {e}")
        
        return []
    
    def generate_learning_roadmap_with_ai(self, goal: str, missing_skills: List[str], weekly_hours: int) -> List[Dict[str, Any]]:
        """Generate AI-powered learning roadmap"""
        
        prompt = f"""
        Create a detailed learning roadmap for transitioning to a {goal} role.
        
        Missing skills: {missing_skills}
        Available time: {weekly_hours} hours per week
        Timeline: 6 weeks
        
        For each week, provide:
        1. Week number
        2. Main topic/focus
        3. Specific resources (courses, tutorials, projects)
        4. Learning goals
        5. Estimated hours
        6. Mastery points to earn
        
        Return JSON format:
        [
            {{
                "week": 1,
                "topic": "Week 1 Topic",
                "resource": "Specific resource name",
                "goal": "Learning objective with mastery points",
                "hours": 5
            }}
        ]
        """
        
        response = self._make_request(prompt, max_tokens=1500)
        
        try:
            roadmap = json.loads(response)
            if isinstance(roadmap, list):
                return roadmap
        except json.JSONDecodeError as e:
            print(f"Error parsing roadmap: {e}")
        
        return []
    
    def _fallback_gap_analysis(self, known_skills: List[str], target_role: str) -> List[SkillGap]:
        """Fallback gap analysis when AI fails"""
        # This would use the existing rule-based logic
        from .gaps import detect_skill_gaps, map_role_to_required_skills
        
        required_skills = map_role_to_required_skills(target_role)
        gaps = detect_skill_gaps(known_skills, required_skills, target_role)
        return gaps

# Global instance
nemotron_service = None

def get_nemotron_service() -> NemotronService:
    """Get or create Nemotron service instance"""
    global nemotron_service
    if nemotron_service is None:
        nemotron_service = NemotronService()
    return nemotron_service
