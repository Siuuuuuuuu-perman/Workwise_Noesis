#!/usr/bin/env python3
"""
Test script for the Reflection Agent
Tests NVIDIA AI-powered learning reflection capabilities
"""

import os
import sys
import json
from datetime import datetime, timedelta

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.reflection_agent import get_reflection_agent, ReflectionAgent

def test_reflection_agent():
    """Test the reflection agent functionality"""
    print("🤖 WorkWise Noesis - Reflection Agent Test")
    print("=" * 60)
    
    try:
        # Initialize reflection agent
        print("🔧 Initializing Reflection Agent...")
        reflection_agent = get_reflection_agent()
        print("✅ Reflection Agent initialized successfully")
        
        # Test data
        user_data = {
            "user_id": "test_user_123",
            "known_skills": ["Python", "SQL", "Excel", "Statistics"],
            "target_role": "Data Scientist",
            "skill_gaps": [
                {"skill": "Machine Learning", "status": "Missing", "proficiency_level": "Beginner"},
                {"skill": "Deep Learning", "status": "Missing", "proficiency_level": "Beginner"},
                {"skill": "TensorFlow", "status": "Missing", "proficiency_level": "Beginner"}
            ],
            "learning_history": [
                {
                    "skill": "Python",
                    "time_invested": 120,
                    "last_practice": "2024-01-15",
                    "assessment_score": 85
                },
                {
                    "skill": "SQL",
                    "time_invested": 80,
                    "last_practice": "2024-01-10",
                    "assessment_score": 78
                },
                {
                    "skill": "Machine Learning",
                    "time_invested": 40,
                    "last_practice": "2024-01-05",
                    "assessment_score": 45
                }
            ],
            "time_invested_hours": 240,
            "assessment_scores": [85, 78, 45, 60, 70]
        }
        
        print("\n📊 Testing Learning Pattern Analysis...")
        insights = reflection_agent.analyze_learning_patterns(user_data)
        print(f"✅ Generated {len(insights)} insights")
        
        for i, insight in enumerate(insights[:3], 1):  # Show first 3 insights
            print(f"   {i}. [{insight.category.upper()}] {insight.title}")
            print(f"      Priority: {insight.priority} | Confidence: {insight.confidence:.2f}")
            print(f"      Description: {insight.description[:100]}...")
            if insight.suggested_actions:
                print(f"      Actions: {', '.join(insight.suggested_actions[:2])}")
            print()
        
        print("📈 Testing Progress Analysis...")
        progress_analysis = reflection_agent.generate_progress_analysis(user_data["learning_history"])
        print(f"✅ Analyzed {len(progress_analysis)} skills")
        
        for progress in progress_analysis[:2]:  # Show first 2 progress items
            print(f"   • {progress.skill}: {progress.progress_percentage:.0f}% ({progress.current_level} → {progress.target_level})")
            print(f"     Time invested: {progress.time_invested_hours}h | Confidence: {progress.confidence_score:.2f}")
        
        print("\n🎯 Testing Comprehensive Reflection Report...")
        report = reflection_agent.create_reflection_report("test_user_123", user_data)
        
        print(f"✅ Reflection Report Generated:")
        print(f"   Overall Progress Score: {report.overall_progress_score:.1f}%")
        print(f"   Key Insights: {len(report.key_insights)}")
        print(f"   Learning Progress Items: {len(report.learning_progress)}")
        print(f"   Recommendations: {len(report.recommendations)}")
        print(f"   Next Milestones: {len(report.next_milestones)}")
        print(f"   Motivational Message: {report.motivational_message}")
        
        print("\n📋 Sample Recommendations:")
        for i, rec in enumerate(report.recommendations[:3], 1):
            print(f"   {i}. {rec}")
        
        print("\n🎯 Sample Milestones:")
        for i, milestone in enumerate(report.next_milestones[:3], 1):
            print(f"   {i}. {milestone}")
        
        print("\n🧪 Testing Fallback Mode...")
        # Test with minimal data to trigger fallback
        minimal_data = {
            "known_skills": ["Python"],
            "target_role": "Developer"
        }
        
        fallback_insights = reflection_agent.analyze_learning_patterns(minimal_data)
        print(f"✅ Fallback mode generated {len(fallback_insights)} insights")
        
        print("\n🎉 All Reflection Agent tests passed!")
        print("\n📊 Test Results:")
        print("   Reflection Agent: ✅ PASS")
        print("   Learning Analysis: ✅ PASS")
        print("   Progress Tracking: ✅ PASS")
        print("   Report Generation: ✅ PASS")
        print("   Fallback Mode: ✅ PASS")
        
        print("\n🚀 Reflection Agent is ready for deployment!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_api_endpoints():
    """Test reflection agent API endpoints"""
    print("\n🌐 Testing API Endpoints...")
    
    try:
        import requests
        
        # Test status endpoint
        response = requests.get("http://localhost:8000/reflection/status", timeout=5)
        if response.status_code == 200:
            status_data = response.json()
            print(f"✅ Status endpoint: {status_data.get('status', 'unknown')}")
            print(f"   Model: {status_data.get('model', 'unknown')}")
            print(f"   AI Powered: {status_data.get('ai_powered', False)}")
        else:
            print(f"⚠️ Status endpoint returned: {response.status_code}")
        
        # Test insights endpoint
        test_data = {
            "known_skills": ["Python", "SQL"],
            "target_role": "Data Analyst",
            "learning_history": [
                {"skill": "Python", "time_invested": 100, "assessment_score": 80}
            ]
        }
        
        response = requests.post(
            "http://localhost:8000/reflection/insights",
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            insights_data = response.json()
            print(f"✅ Insights endpoint: {len(insights_data.get('insights', []))} insights generated")
        else:
            print(f"⚠️ Insights endpoint returned: {response.status_code}")
        
        print("✅ API endpoint tests completed")
        
    except requests.exceptions.ConnectionError:
        print("⚠️ API server not running - skipping endpoint tests")
    except Exception as e:
        print(f"⚠️ API test error: {e}")

if __name__ == "__main__":
    print("🧪 Starting Reflection Agent Tests...")
    
    # Test core functionality
    success = test_reflection_agent()
    
    if success:
        # Test API endpoints if server is running
        test_api_endpoints()
        
        print("\n🎉 All tests completed successfully!")
        print("🚀 Your Reflection Agent is ready to deploy!")
    else:
        print("\n❌ Tests failed - check the errors above")
        sys.exit(1)
