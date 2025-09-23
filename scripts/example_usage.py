#!/usr/bin/env python3
"""
Example usage of the Restaurant Finder with Gemini AI integration.
"""

import os
import sys
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api.gemini_client import GeminiClient


def main():
    """Example usage of GeminiClient."""
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable")
        print("You can run: export GEMINI_API_KEY='your_api_key_here'")
        return
    
    # Initialize client
    print("🍽️ Restaurant Finder - Gemini AI Example")
    print("=" * 50)
    
    try:
        client = GeminiClient(api_key)
        print("✅ Gemini client initialized")
        
        # Test connection
        if client.test_connection():
            print("✅ API connection successful")
        else:
            print("❌ API connection failed")
            return
        
        # Example 1: Basic text generation
        print("\n📝 Example 1: Basic Text Generation")
        print("-" * 30)
        response = client.generate_text("What are the best Italian restaurants in Los Angeles?")
        print(f"Response: {response}")
        
        # Example 2: Request reformatting
        print("\n🔄 Example 2: Request Reformatter")
        print("-" * 30)
        user_requests = [
            "Find me a cheap Chinese restaurant less than a 20 minute drive from me",
            "I want expensive sushi with good ratings",
            "Show me Italian food near downtown LA"
        ]
        
        for request in user_requests:
            print(f"\nUser request: {request}")
            formatted = client.request_reformatter(request)
            print(f"Formatted: {json.dumps(formatted, indent=2)}")
        
        # Example 3: Restaurant recommendations
        print("\n🍽️ Example 3: Restaurant Recommendations")
        print("-" * 30)
        criteria = {
            "cuisine": "Italian",
            "price_range": "moderate",
            "location": "Los Angeles, CA",
            "rating_min": 4.0,
            "features": ["outdoor_seating", "family_friendly"]
        }
        
        recommendations = client.generate_restaurant_recommendations(criteria)
        print(f"Recommendations:\n{recommendations}")
        
        print("\n🎉 All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
