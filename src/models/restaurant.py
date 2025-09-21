"""
Restaurant data model.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class Restaurant:
    """Data model for restaurant information."""
    
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone: Optional[str] = None
    cuisine_type: Optional[str] = None
    price_range: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    hours: Optional[Dict[str, str]] = None
    website: Optional[str] = None
    description: Optional[str] = None
    
    def __post_init__(self):
        """Validate data after initialization."""
        if not self.name or not self.address:
            raise ValueError("Restaurant name and address are required")
        
        if self.rating is not None and (self.rating < 0 or self.rating > 5):
            raise ValueError("Rating must be between 0 and 5")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert restaurant to dictionary."""
        return {
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'phone': self.phone,
            'cuisine_type': self.cuisine_type,
            'price_range': self.price_range,
            'rating': self.rating,
            'review_count': self.review_count,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'hours': self.hours,
            'website': self.website,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Restaurant':
        """Create restaurant from dictionary."""
        return cls(**data)
    
    def get_full_address(self) -> str:
        """Get formatted full address."""
        return f"{self.address}, {self.city}, {self.state} {self.zip_code}"
    
    def get_rating_display(self) -> str:
        """Get formatted rating display."""
        if self.rating is None:
            return "No rating"
        return f"{self.rating:.1f}/5.0"
    
    def is_open_now(self) -> Optional[bool]:
        """Check if restaurant is currently open."""
        if not self.hours:
            return None
        
        # TODO: Implement actual hours checking logic
        # This would parse the hours and check against current time
        return None
