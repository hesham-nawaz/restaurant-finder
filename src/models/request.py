"""
Request and response models for the restaurant finder API.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum


class PriceRange(Enum):
    """Price range enumeration."""
    BUDGET = "budget"
    MODERATE = "moderate"
    EXPENSIVE = "expensive"
    VERY_EXPENSIVE = "very_expensive"


class CuisineType(Enum):
    """Cuisine type enumeration."""
    AMERICAN = "american"
    CHINESE = "chinese"
    ITALIAN = "italian"
    MEXICAN = "mexican"
    JAPANESE = "japanese"
    INDIAN = "indian"
    THAI = "thai"
    FRENCH = "french"
    MEDITERRANEAN = "mediterranean"
    OTHER = "other"


@dataclass
class RestaurantRequest:
    """Model for restaurant search requests."""
    
    location: str
    cuisine: Optional[CuisineType] = None
    price_range: Optional[PriceRange] = None
    rating_min: Optional[float] = None
    max_distance: Optional[float] = None  # in miles
    max_time: Optional[int] = None  # in minutes
    features: Optional[List[str]] = None  # e.g., ["delivery", "outdoor_seating"]
    
    def __post_init__(self):
        """Validate request data."""
        if not self.location:
            raise ValueError("Location is required")
        
        if self.rating_min is not None and (self.rating_min < 0 or self.rating_min > 5):
            raise ValueError("Rating must be between 0 and 5")
        
        if self.max_distance is not None and self.max_distance < 0:
            raise ValueError("Max distance must be positive")
        
        if self.max_time is not None and self.max_time < 0:
            raise ValueError("Max time must be positive")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert request to dictionary."""
        return {
            'location': self.location,
            'cuisine': self.cuisine.value if self.cuisine else None,
            'price_range': self.price_range.value if self.price_range else None,
            'rating_min': self.rating_min,
            'max_distance': self.max_distance,
            'max_time': self.max_time,
            'features': self.features
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RestaurantRequest':
        """Create request from dictionary."""
        # Convert string enums back to enum objects
        if data.get('cuisine'):
            data['cuisine'] = CuisineType(data['cuisine'])
        if data.get('price_range'):
            data['price_range'] = PriceRange(data['price_range'])
        
        return cls(**data)


@dataclass
class RestaurantResponse:
    """Model for restaurant search responses."""
    
    restaurants: List[Dict[str, Any]]
    total_count: int
    search_criteria: RestaurantRequest
    search_time: float  # in seconds
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            'restaurants': self.restaurants,
            'total_count': self.total_count,
            'search_criteria': self.search_criteria.to_dict(),
            'search_time': self.search_time
        }
