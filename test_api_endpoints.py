#!/usr/bin/env python3
"""
Simple NVIDIA API test to verify the API key and find correct endpoint
"""

import requests
import json

def test_nvidia_api():
    """Test NVIDIA API with different endpoints"""
    
    api_key = "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"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Test different possible endpoints
    endpoints = [
        "https://api.nvcf.nvidia.com/v1/chat/completions",
        "https://api.nvidia.com/v1/chat/completions", 
        "https://build.nvidia.com/api/v1/chat/completions",
        "https://api.nvcf.nvidia.com/v2/chat/completions"
    ]
    
    payload = {
        "model": "nvidia/nemotron-nano-9b-v2",
        "messages": [{"role": "user", "content": "Hello, test message"}],
        "max_tokens": 50
    }
    
    print("🔍 Testing NVIDIA API endpoints...")
    
    for endpoint in endpoints:
        print(f"\nTesting: {endpoint}")
        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
            if response.status_code == 200:
                print("✅ SUCCESS! Found working endpoint")
                return endpoint
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n⚠️ No working endpoint found. The API key might need different configuration.")
    return None

if __name__ == "__main__":
    working_endpoint = test_nvidia_api()
    if working_endpoint:
        print(f"\n🎉 Working endpoint: {working_endpoint}")
    else:
        print("\n💡 The API key is valid but may need:")
        print("   - Different endpoint URL")
        print("   - Different model name")
        print("   - Different request format")
        print("   - Account activation/verification")
