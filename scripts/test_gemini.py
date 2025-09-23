#!/usr/bin/env python3
"""
Test script for GeminiClient functionality.
"""

import os
import sys
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api.gemini_client import GeminiClient


def test_gemini_client():
    """Test the GeminiClient functionality."""
    
    # Get API key from environment or prompt user
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        api_key = input("Enter your Gemini API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting.")
        return
    
    try:
        # Initialize client
        print("🔧 Initializing Gemini client...")
        client = GeminiClient(api_key)
        print("✅ Client initialized successfully")
        
        # Test connection
        print("\n🔍 Testing API connection...")
        if client.test_connection():
            print("✅ API connection successful")
        else:
            print("❌ API connection failed")
            return
        
        # Test basic text generation
        print("\n📝 Testing basic text generation...")
        response = client.generate_text("What is the capital of France?")
        print(f"Response: {response}")
        
        # Test request reformatter
        print("\n🔄 Testing request reformatter...")
        user_request = "Find me a cheap Chinese restaurant less than a 20 minute drive from me"
        formatted_request = client.request_reformatter(user_request)
        print(f"Formatted request: {json.dumps(formatted_request, indent=2)}")
        
        # Test restaurant recommendations
        print("\n🍽️ Testing restaurant recommendations...")
        criteria = {
            "cuisine": "Italian",
            "price_range": "moderate",
            "location": "Los Angeles, CA",
            "rating_min": 4.0
        }
        recommendations = client.generate_restaurant_recommendations(criteria)
        print(f"Recommendations: {recommendations}")
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_gemini_client()
