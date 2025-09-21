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
            
            # TODO: Use Gemini client to parse user request
            # For now, create a simple request
            request = RestaurantRequest(location="Los Angeles, CA")
            response = restaurant_service.search_restaurants(request)
            
            print(f"Found {response.total_count} restaurants")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
