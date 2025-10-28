"""
Reflection Agent Service - AI-powered learning reflection and guidance
Uses NVIDIA Nemotron for intelligent reflection and personalized insights
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
class ReflectionInsight:
    """Data class for reflection insights"""
    category: str  # "strength", "weakness", "opportunity", "threat"
    title: str
    description: str
    confidence: float  # 0.0 to 1.0
    actionable: bool
    priority: str  # "high", "medium", "low"
    suggested_actions: List[str]

@dataclass
class LearningProgress:
    """Data class for learning progress tracking"""
    skill: str
    current_level: str
    target_level: str
    progress_percentage: float
    time_invested_hours: float
    last_practice_date: Optional[datetime]
    confidence_score: float

@dataclass
class ReflectionReport:
    """Data class for comprehensive reflection report"""
    user_id: str
    generated_at: datetime
    overall_progress_score: float
    key_insights: List[ReflectionInsight]
    learning_progress: List[LearningProgress]
    recommendations: List[str]
    next_milestones: List[str]
    motivational_message: str

class ReflectionAgent:
    """AI-powered reflection agent using NVIDIA Nemotron"""
    
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_API_KEY")
        self.base_url = os.getenv("NVIDIA_BASE_URL", "https://api.nvcf.nvidia.com/v1")
        self.model = os.getenv("NEMOTRON_MODEL", "nvidia/nemotron-nano-9b-v2")
        
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY environment variable is required")
    
    def _make_request(self, prompt: str, max_tokens: int = 2000) -> str:
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
                    "content": "You are an intelligent learning reflection agent. Provide thoughtful, actionable insights for skill development and learning progress."
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
    
    def analyze_learning_patterns(self, user_data: Dict[str, Any]) -> List[ReflectionInsight]:
        """Analyze user's learning patterns and generate insights"""
        prompt = f"""
        Analyze the following learning data and provide insights using SWOT analysis framework.
        Return a JSON array of insights with this structure:
        [
            {{
                "category": "strength|weakness|opportunity|threat",
                "title": "Brief title",
                "description": "Detailed description",
                "confidence": 0.0-1.0,
                "actionable": true/false,
                "priority": "high|medium|low",
                "suggested_actions": ["action1", "action2"]
            }}
        ]
        
        User Data:
        - Known Skills: {user_data.get('known_skills', [])}
        - Target Role: {user_data.get('target_role', 'Unknown')}
        - Skill Gaps: {user_data.get('skill_gaps', [])}
        - Learning History: {user_data.get('learning_history', [])}
        - Time Invested: {user_data.get('time_invested_hours', 0)}
        - Assessment Scores: {user_data.get('assessment_scores', [])}
        
        Focus on actionable insights that can guide learning decisions.
        """
        
        try:
            response_text = self._make_request(prompt, max_tokens=1500)
            insights_data = json.loads(response_text)
            
            insights = []
            for insight_data in insights_data:
                insight = ReflectionInsight(
                    category=insight_data.get("category", "opportunity"),
                    title=insight_data.get("title", "Learning Insight"),
                    description=insight_data.get("description", ""),
                    confidence=float(insight_data.get("confidence", 0.5)),
                    actionable=insight_data.get("actionable", True),
                    priority=insight_data.get("priority", "medium"),
                    suggested_actions=insight_data.get("suggested_actions", [])
                )
                insights.append(insight)
            
            return insights
            
        except (json.JSONDecodeError, requests.exceptions.RequestException, ValueError) as e:
            print(f"⚠️ NVIDIA API failed, using fallback insights: {e}")
            # Return fallback insights
            return self._get_fallback_insights(user_data)
    
    def generate_progress_analysis(self, learning_data: List[Dict[str, Any]]) -> List[LearningProgress]:
        """Generate detailed progress analysis for each skill"""
        prompt = f"""
        Analyze the learning progress for each skill and provide detailed progress tracking.
        Return a JSON array with this structure:
        [
            {{
                "skill": "skill_name",
                "current_level": "Beginner|Intermediate|Advanced|Expert",
                "target_level": "Beginner|Intermediate|Advanced|Expert",
                "progress_percentage": 0-100,
                "time_invested_hours": number,
                "last_practice_date": "YYYY-MM-DD or null",
                "confidence_score": 0.0-1.0
            }}
        ]
        
        Learning Data: {json.dumps(learning_data, indent=2)}
        
        Calculate realistic progress based on time invested and assessment performance.
        """
        
        try:
            response_text = self._make_request(prompt, max_tokens=1200)
            progress_data = json.loads(response_text)
            
            progress_list = []
            for progress_item in progress_data:
                progress = LearningProgress(
                    skill=progress_item.get("skill", "Unknown"),
                    current_level=progress_item.get("current_level", "Beginner"),
                    target_level=progress_item.get("target_level", "Intermediate"),
                    progress_percentage=float(progress_item.get("progress_percentage", 0)),
                    time_invested_hours=float(progress_item.get("time_invested_hours", 0)),
                    last_practice_date=datetime.fromisoformat(progress_item.get("last_practice_date")) if progress_item.get("last_practice_date") else None,
                    confidence_score=float(progress_item.get("confidence_score", 0.5))
                )
                progress_list.append(progress)
            
            return progress_list
            
        except (json.JSONDecodeError, requests.exceptions.RequestException, ValueError) as e:
            print(f"⚠️ NVIDIA API failed, using fallback progress: {e}")
            return self._get_fallback_progress(learning_data)
    
    def create_reflection_report(self, user_id: str, user_data: Dict[str, Any]) -> ReflectionReport:
        """Create a comprehensive reflection report"""
        print(f"🤖 Creating reflection report for user {user_id}")
        
        # Analyze learning patterns
        insights = self.analyze_learning_patterns(user_data)
        
        # Generate progress analysis
        learning_data = user_data.get('learning_history', [])
        progress_analysis = self.generate_progress_analysis(learning_data)
        
        # Calculate overall progress score
        overall_score = self._calculate_overall_progress(progress_analysis)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(insights, progress_analysis)
        
        # Generate next milestones
        milestones = self._generate_milestones(progress_analysis, user_data.get('target_role', ''))
        
        # Generate motivational message
        motivational_message = self._generate_motivational_message(overall_score, insights)
        
        report = ReflectionReport(
            user_id=user_id,
            generated_at=datetime.now(),
            overall_progress_score=overall_score,
            key_insights=insights,
            learning_progress=progress_analysis,
            recommendations=recommendations,
            next_milestones=milestones,
            motivational_message=motivational_message
        )
        
        print(f"✅ Reflection report created with {len(insights)} insights and {len(progress_analysis)} progress items")
        return report
    
    def _calculate_overall_progress(self, progress_analysis: List[LearningProgress]) -> float:
        """Calculate overall progress score"""
        if not progress_analysis:
            return 0.0
        
        total_progress = sum(p.progress_percentage for p in progress_analysis)
        return total_progress / len(progress_analysis)
    
    def _generate_recommendations(self, insights: List[ReflectionInsight], progress: List[LearningProgress]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # High priority actionable insights
        high_priority = [i for i in insights if i.priority == "high" and i.actionable]
        for insight in high_priority[:3]:  # Top 3
            recommendations.extend(insight.suggested_actions)
        
        # Progress-based recommendations
        low_progress = [p for p in progress if p.progress_percentage < 30]
        if low_progress:
            recommendations.append(f"Focus on {low_progress[0].skill} - currently at {low_progress[0].progress_percentage:.0f}% progress")
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def _generate_milestones(self, progress: List[LearningProgress], target_role: str) -> List[str]:
        """Generate next learning milestones"""
        milestones = []
        
        for p in progress:
            if p.progress_percentage < 50:
                milestones.append(f"Complete {p.skill} fundamentals (target: {p.target_level})")
            elif p.progress_percentage < 80:
                milestones.append(f"Master {p.skill} intermediate concepts")
            else:
                milestones.append(f"Apply {p.skill} in real-world projects")
        
        return milestones[:4]  # Limit to 4 milestones
    
    def _generate_motivational_message(self, overall_score: float, insights: List[ReflectionInsight]) -> str:
        """Generate personalized motivational message"""
        if overall_score >= 80:
            return "🎉 Excellent progress! You're on track to achieve your learning goals. Keep up the great work!"
        elif overall_score >= 60:
            return "🚀 Great progress! You're making solid headway. Focus on your weak areas to accelerate growth."
        elif overall_score >= 40:
            return "💪 Good start! You're building momentum. Consistency is key - keep practicing regularly."
        else:
            return "🌟 Every expert was once a beginner. You're taking the right steps - keep going!"
    
    def _get_fallback_insights(self, user_data: Dict[str, Any]) -> List[ReflectionInsight]:
        """Fallback insights when AI fails"""
        return [
            ReflectionInsight(
                category="opportunity",
                title="Consistent Practice",
                description="Regular practice sessions will accelerate your learning progress",
                confidence=0.8,
                actionable=True,
                priority="high",
                suggested_actions=["Schedule daily practice sessions", "Set specific learning goals"]
            ),
            ReflectionInsight(
                category="strength",
                title="Learning Commitment",
                description="Your dedication to skill development is commendable",
                confidence=0.9,
                actionable=False,
                priority="medium",
                suggested_actions=["Maintain current learning pace"]
            )
        ]
    
    def _get_fallback_progress(self, learning_data: List[Dict[str, Any]]) -> List[LearningProgress]:
        """Fallback progress when AI fails"""
        progress_list = []
        for item in learning_data[:5]:  # Limit to 5 items
            progress = LearningProgress(
                skill=item.get("skill", "Unknown"),
                current_level="Beginner",
                target_level="Intermediate",
                progress_percentage=25.0,
                time_invested_hours=item.get("time_invested", 0),
                last_practice_date=None,
                confidence_score=0.5
            )
            progress_list.append(progress)
        return progress_list

# Global instance
_reflection_agent_instance = None

def get_reflection_agent():
    """Get or create reflection agent instance"""
    global _reflection_agent_instance
    if _reflection_agent_instance is None:
        _reflection_agent_instance = ReflectionAgent()
    return _reflection_agent_instance
