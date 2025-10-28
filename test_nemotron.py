#!/usr/bin/env python3
"""
Test script for NVIDIA Nemotron integration
Run this to test the Nemotron Nano v12 model integration
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_nemotron_integration():
    """Test the Nemotron integration"""
    
    print("🚀 Testing NVIDIA Nemotron Integration")
    print("=" * 50)
    
    # Check environment variables
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        print("❌ NVIDIA_API_KEY not found in environment variables")
        print("Please set your NVIDIA API key:")
        print("export NVIDIA_API_KEY='your_api_key_here'")
        return False
    
    print(f"✅ NVIDIA API Key found: {api_key[:10]}...")
    
    # Test Nemotron service
    try:
        from backend.app.services.nemotron import get_nemotron_service
        
        print("\n🔧 Initializing Nemotron service...")
        nemotron = get_nemotron_service()
        print("✅ Nemotron service initialized successfully")
        
        # Test skill extraction
        print("\n📝 Testing skill extraction...")
        test_text = """
        I am a software engineer with 5 years of experience in Python, JavaScript, and React. 
        I have worked with databases like PostgreSQL and MongoDB. I'm familiar with machine learning 
        using TensorFlow and scikit-learn. I also have experience with cloud platforms like AWS and Docker.
        """
        
        skills = nemotron.extract_skills_from_text(test_text, ["Python", "JavaScript"])
        print(f"✅ Extracted skills: {skills}")
        
        # Test gap analysis
        print("\n🎯 Testing skill gap analysis...")
        gaps = nemotron.analyze_skill_gaps_with_ai(skills, "Data Analyst")
        print(f"✅ Found {len(gaps)} skill gaps")
        for gap in gaps[:3]:  # Show first 3
            print(f"   - {gap.skill}: {gap.status} ({gap.proficiency_level} → {gap.required_proficiency})")
        
        # Test assessment generation
        print("\n📋 Testing assessment generation...")
        questions = nemotron.generate_assessment_questions(["Python", "SQL"], 2)
        print(f"✅ Generated {len(questions)} assessment questions")
        if questions:
            print(f"   Sample question: {questions[0]['prompt'][:50]}...")
        
        print("\n🎉 All tests passed! Nemotron integration is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Nemotron integration: {e}")
        return False

def test_fallback_mode():
    """Test fallback mode when Nemotron is not available"""
    
    print("\n🔄 Testing fallback mode...")
    
    try:
        from backend.app.services.skills import extract_skills_from_text
        
        test_text = "I know Python, SQL, and Excel"
        skills = extract_skills_from_text(test_text, ["Python"])
        print(f"✅ Fallback skill extraction: {skills}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing fallback mode: {e}")
        return False

if __name__ == "__main__":
    print("🧪 WorkWise Noesis - Nemotron Integration Test")
    print("=" * 60)
    
    # Test Nemotron integration
    nemotron_success = test_nemotron_integration()
    
    # Test fallback mode
    fallback_success = test_fallback_mode()
    
    print("\n📊 Test Results:")
    print(f"   Nemotron Integration: {'✅ PASS' if nemotron_success else '❌ FAIL'}")
    print(f"   Fallback Mode: {'✅ PASS' if fallback_success else '❌ FAIL'}")
    
    if nemotron_success:
        print("\n🚀 Ready to deploy with Nemotron AI!")
    elif fallback_success:
        print("\n⚠️ Running in fallback mode (rule-based)")
    else:
        print("\n❌ Integration failed - check your configuration")
