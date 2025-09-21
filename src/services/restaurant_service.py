"""
Restaurant recommendation service.
"""

import pandas as pd
import os
from typing import List, Dict, Any, Optional
from ..models.restaurant import Restaurant
from ..models.request import RestaurantRequest, RestaurantResponse


class RestaurantService:
    """Service for restaurant recommendations and data processing."""
    
    def __init__(self, data_path: str = "data/raw"):
        """
        Initialize the restaurant service.
        
        Args:
            data_path: Path to restaurant data files
        """
        self.data_path = data_path
        self.restaurants_df: Optional[pd.DataFrame] = None
        self._load_data()
    
    def _load_data(self) -> None:
        """Load restaurant data from CSV files."""
        try:
            # Find the most recent CSV file
            csv_files = [f for f in os.listdir(self.data_path) if f.endswith('.csv')]
            if not csv_files:
                raise FileNotFoundError(f"No CSV files found in {self.data_path}")
            
            latest_file = sorted(csv_files)[-1]
            file_path = os.path.join(self.data_path, latest_file)
            
            self.restaurants_df = pd.read_csv(file_path)
            print(f"✅ Loaded {len(self.restaurants_df)} restaurants from {latest_file}")
            
        except Exception as e:
            print(f"❌ Error loading restaurant data: {e}")
            self.restaurants_df = None
    
    def search_restaurants(self, request: RestaurantRequest) -> RestaurantResponse:
        """
        Search for restaurants based on criteria.
        
        Args:
            request: Restaurant search request
            
        Returns:
            Restaurant search response
        """
        if self.restaurants_df is None:
            raise ValueError("Restaurant data not loaded")
        
        import time
        start_time = time.time()
        
        # Start with all restaurants
        filtered_df = self.restaurants_df.copy()
        
        # Apply filters based on request criteria
        if request.cuisine:
            filtered_df = filtered_df[
                filtered_df['cuisine_type'].str.contains(request.cuisine.value, case=False, na=False)
            ]
        
        if request.price_range:
            # Map price range to actual price values
            price_mapping = {
                'budget': ['$', '$$'],
                'moderate': ['$$', '$$$'],
                'expensive': ['$$$', '$$$$'],
                'very_expensive': ['$$$$']
            }
            valid_prices = price_mapping.get(request.price_range.value, [])
            filtered_df = filtered_df[filtered_df['price_range'].isin(valid_prices)]
        
        if request.rating_min:
            filtered_df = filtered_df[filtered_df['rating'] >= request.rating_min]
        
        # Convert to list of dictionaries
        restaurants = filtered_df.to_dict('records')
        
        search_time = time.time() - start_time
        
        return RestaurantResponse(
            restaurants=restaurants,
            total_count=len(restaurants),
            search_criteria=request,
            search_time=search_time
        )
    
    def get_restaurant_by_id(self, restaurant_id: str) -> Optional[Restaurant]:
        """
        Get a specific restaurant by ID.
        
        Args:
            restaurant_id: Restaurant identifier
            
        Returns:
            Restaurant object or None if not found
        """
        if self.restaurants_df is None:
            return None
        
        restaurant_data = self.restaurants_df[
            self.restaurants_df['id'] == restaurant_id
        ]
        
        if restaurant_data.empty:
            return None
        
        return Restaurant.from_dict(restaurant_data.iloc[0].to_dict())
    
    def get_popular_restaurants(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get popular restaurants based on rating and review count.
        
        Args:
            limit: Maximum number of restaurants to return
            
        Returns:
            List of popular restaurants
        """
        if self.restaurants_df is None:
            return []
        
        # Sort by rating and review count
        popular = self.restaurants_df.nlargest(limit, ['rating', 'review_count'])
        return popular.to_dict('records')
    
    def get_restaurants_by_cuisine(self, cuisine: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get restaurants by cuisine type.
        
        Args:
            cuisine: Cuisine type
            limit: Maximum number of restaurants to return
            
        Returns:
            List of restaurants
        """
        if self.restaurants_df is None:
            return []
        
        filtered = self.restaurants_df[
            self.restaurants_df['cuisine_type'].str.contains(cuisine, case=False, na=False)
        ]
        
        return filtered.head(limit).to_dict('records')
    
    def get_data_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of the restaurant data.
        
        Returns:
            Dictionary with data summary
        """
        if self.restaurants_df is None:
            return {"error": "No data loaded"}
        
        return {
            "total_restaurants": len(self.restaurants_df),
            "cuisine_types": self.restaurants_df['cuisine_type'].value_counts().to_dict(),
            "price_ranges": self.restaurants_df['price_range'].value_counts().to_dict(),
            "average_rating": self.restaurants_df['rating'].mean(),
            "rating_distribution": self.restaurants_df['rating'].value_counts().to_dict()
        }
