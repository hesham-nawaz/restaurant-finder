"""
Main application entry point for Restaurant Finder.
"""

import os
import sys
from typing import Optional

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.gemini_client import GeminiClient
from api.aws_client import AWSClient
from services.restaurant_service import RestaurantService
from services.prompt_service import PromptService
from models.request import RestaurantRequest, CuisineType, PriceRange


def main():
    """Main application function."""
    print("🍽️  Restaurant Finder - AI-Powered Recommendations")
    print("=" * 50)
    
    # Initialize services
    try:
        # Initialize prompt service
        prompt_service = PromptService()
        print("✅ Prompt service initialized")
        
        # Initialize restaurant service
        restaurant_service = RestaurantService()
        print("✅ Restaurant service initialized")
        
        # Initialize Gemini client (optional - only if API key is available)
        gemini_client = None
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if gemini_api_key:
            try:
                gemini_client = GeminiClient(gemini_api_key)
                if gemini_client.test_connection():
                    print("✅ Gemini client initialized and connected")
                else:
                    print("⚠️ Gemini client initialized but connection test failed")
                    gemini_client = None
            except Exception as e:
                print(f"⚠️ Failed to initialize Gemini client: {e}")
                gemini_client = None
        else:
            print("⚠️ GEMINI_API_KEY not found - AI features disabled")
        
        # Get data summary
        summary = restaurant_service.get_data_summary()
        print(f"📊 Loaded {summary.get('total_restaurants', 0)} restaurants")
        
    except Exception as e:
        print(f"❌ Error initializing services: {e}")
        return
    
    # Example usage
    print("\n🔍 Example: Searching for Chinese restaurants...")
    
    try:
        # Create a search request
        request = RestaurantRequest(
            location="Los Angeles, CA",
            cuisine=CuisineType.CHINESE,
            price_range=PriceRange.MODERATE,
            rating_min=4.0
        )
        
        # Search for restaurants
        response = restaurant_service.search_restaurants(request)
        
        print(f"Found {response.total_count} restaurants matching criteria")
        print(f"Search completed in {response.search_time:.2f} seconds")
        
        # Display first few results
        if response.restaurants:
            print("\n🏆 Top Results:")
            for i, restaurant in enumerate(response.restaurants[:3], 1):
                print(f"{i}. {restaurant.get('name', 'Unknown')} - {restaurant.get('rating', 'N/A')}/5.0")
                print(f"   {restaurant.get('address', 'Unknown address')}")
                print(f"   Cuisine: {restaurant.get('cuisine_type', 'Unknown')}")
                print()
        
    except Exception as e:
        print(f"❌ Error during search: {e}")
    
    # Interactive mode
    print("\n💬 Interactive Mode:")
    print("Enter your restaurant search request (or 'quit' to exit):")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Use Gemini client to parse user request if available
            if gemini_client:
                try:
                    # Parse user request using AI
                    parsed_request = gemini_client.request_reformatter(user_input)
                    print(f"🤖 AI parsed request: {parsed_request}")
                    
                    # Create RestaurantRequest from parsed data
                    request = RestaurantRequest(
                        location=parsed_request.get('location', 'Los Angeles, CA'),
                        cuisine=CuisineType(parsed_request['cuisine']) if parsed_request.get('cuisine') else None,
                        price_range=PriceRange(parsed_request['price']) if parsed_request.get('price') else None,
                        rating_min=parsed_request.get('rating')
                    )
                    
                    # Search for restaurants
                    response = restaurant_service.search_restaurants(request)
                    print(f"Found {response.total_count} restaurants matching your criteria")
                    
                    # Generate AI recommendations
                    if response.restaurants:
                        criteria = {
                            'location': request.location,
                            'cuisine': request.cuisine.value if request.cuisine else None,
                            'price_range': request.price_range.value if request.price_range else None,
                            'rating_min': request.rating_min
                        }
                        ai_recommendations = gemini_client.generate_restaurant_recommendations(criteria)
                        print(f"\n🤖 AI Recommendations:\n{ai_recommendations}")
                    
                except Exception as e:
                    print(f"❌ Error processing AI request: {e}")
                    # Fallback to simple search
                    request = RestaurantRequest(location="Los Angeles, CA")
                    response = restaurant_service.search_restaurants(request)
                    print(f"Found {response.total_count} restaurants (fallback search)")
            else:
                # Fallback when Gemini is not available
                request = RestaurantRequest(location="Los Angeles, CA")
                response = restaurant_service.search_restaurants(request)
                print(f"Found {response.total_count} restaurants (AI not available)")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
