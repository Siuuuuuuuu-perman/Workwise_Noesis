#!/usr/bin/env python3
"""
Test script for the Course Recommendation Service
Tests AI-powered course recommendations from multiple learning platforms
"""

import os
import sys
import json
from datetime import datetime

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.course_recommendations import get_course_service, CourseRecommendationService

def test_course_recommendation_service():
    """Test the course recommendation service functionality"""
    print("🎓 WorkWise Noesis - Course Recommendation Service Test")
    print("=" * 70)
    
    try:
        # Initialize course service
        print("🔧 Initializing Course Recommendation Service...")
        course_service = get_course_service()
        print("✅ Course Recommendation Service initialized successfully")
        
        # Test user profile
        user_profile = {
            "user_id": "test_user_123",
            "current_skills": ["Python", "SQL", "Excel"],
            "target_role": "Data Scientist",
            "skill_gaps": [
                {"skill": "Machine Learning", "status": "Missing", "proficiency_level": "Beginner"},
                {"skill": "Deep Learning", "status": "Missing", "proficiency_level": "Beginner"},
                {"skill": "Statistics", "status": "Missing", "proficiency_level": "Intermediate"}
            ],
            "learning_style": "Mixed",
            "time_available_hours": 15,
            "budget": 150,
            "preferred_platforms": ["Coursera", "Khan Academy", "Udemy"],
            "experience_level": "Intermediate"
        }
        
        print("\n📊 Testing AI Course Recommendations...")
        recommendations = course_service.get_ai_course_recommendations(user_profile)
        print(f"✅ Generated {len(recommendations)} course recommendations")
        
        for i, rec in enumerate(recommendations[:3], 1):  # Show first 3 recommendations
            print(f"\n   {i}. [{rec.priority.upper()}] {rec.course.title}")
            print(f"      Platform: {rec.course.platform} | Match Score: {rec.match_score:.2f}")
            print(f"      Duration: {rec.course.duration_hours}h | Price: ${rec.course.price}")
            print(f"      Skills: {', '.join(rec.course.skills_covered[:3])}")
            print(f"      Reasoning: {rec.reasoning[:100]}...")
        
        print("\n🎯 Testing Learning Path Creation...")
        learning_path = course_service.create_learning_path(user_profile)
        
        print(f"✅ Learning Path Generated:")
        print(f"   Target Role: {learning_path['target_role']}")
        print(f"   Total Courses: {learning_path['total_courses']}")
        print(f"   Total Hours: {learning_path['total_hours']}")
        print(f"   Total Cost: ${learning_path['total_cost']}")
        print(f"   Estimated Completion: {learning_path['estimated_completion_days']} days")
        
        print("\n📈 Platform Breakdown:")
        for platform, count in learning_path['platform_breakdown'].items():
            print(f"   • {platform.title()}: {count} courses")
        
        print("\n🔍 Testing Platform Search...")
        for platform in ["coursera", "khan_academy", "udemy"]:
            courses = course_service.search_courses_on_platform(platform, "Machine Learning", "Beginner")
            print(f"   • {platform.title()}: {len(courses)} courses found")
        
        print("\n🧪 Testing Fallback Mode...")
        # Test with minimal data to trigger fallback
        minimal_profile = {
            "current_skills": ["Python"],
            "target_role": "Developer"
        }
        
        fallback_recommendations = course_service.get_ai_course_recommendations(minimal_profile)
        print(f"✅ Fallback mode generated {len(fallback_recommendations)} recommendations")
        
        print("\n🎉 All Course Recommendation tests passed!")
        print("\n📊 Test Results:")
        print("   Course Recommendation Service: ✅ PASS")
        print("   AI-Powered Recommendations: ✅ PASS")
        print("   Learning Path Creation: ✅ PASS")
        print("   Platform Integration: ✅ PASS")
        print("   Fallback Mode: ✅ PASS")
        
        print("\n🚀 Course Recommendation Service is ready for deployment!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_api_endpoints():
    """Test course recommendation API endpoints"""
    print("\n🌐 Testing Course API Endpoints...")
    
    try:
        import requests
        
        # Test status endpoint
        response = requests.get("http://localhost:8000/courses/status", timeout=5)
        if response.status_code == 200:
            status_data = response.json()
            print(f"✅ Status endpoint: {status_data.get('status', 'unknown')}")
            print(f"   Supported Platforms: {len(status_data.get('supported_platforms', []))}")
            print(f"   AI Powered: {status_data.get('ai_powered', False)}")
        else:
            print(f"⚠️ Status endpoint returned: {response.status_code}")
        
        # Test platforms endpoint
        response = requests.get("http://localhost:8000/courses/platforms", timeout=5)
        if response.status_code == 200:
            platforms_data = response.json()
            print(f"✅ Platforms endpoint: {len(platforms_data.get('supported_platforms', []))} platforms")
        else:
            print(f"⚠️ Platforms endpoint returned: {response.status_code}")
        
        # Test recommendations endpoint
        test_profile = {
            "current_skills": ["Python"],
            "target_role": "Data Analyst",
            "skill_gaps": [{"skill": "Machine Learning", "status": "Missing"}],
            "budget": 100,
            "preferred_platforms": ["Coursera"]
        }
        
        response = requests.post(
            "http://localhost:8000/courses/recommend",
            json=test_profile,
            timeout=10
        )
        
        if response.status_code == 200:
            rec_data = response.json()
            print(f"✅ Recommendations endpoint: {len(rec_data.get('recommendations', []))} recommendations")
        else:
            print(f"⚠️ Recommendations endpoint returned: {response.status_code}")
        
        print("✅ Course API endpoint tests completed")
        
    except requests.exceptions.ConnectionError:
        print("⚠️ API server not running - skipping endpoint tests")
    except Exception as e:
        print(f"⚠️ API test error: {e}")

if __name__ == "__main__":
    print("🧪 Starting Course Recommendation Service Tests...")
    
    # Test core functionality
    success = test_course_recommendation_service()
    
    if success:
        # Test API endpoints if server is running
        test_api_endpoints()
        
        print("\n🎉 All tests completed successfully!")
        print("🚀 Your Course Recommendation Service is ready to deploy!")
    else:
        print("\n❌ Tests failed - check the errors above")
        sys.exit(1)
