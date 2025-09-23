from enum import Enum
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, conint, confloat

class DistanceType(str, Enum):
    time = "time"
    geo = "geo"

class Distance(BaseModel):
    type: DistanceType
    value: conint(gt=0)
    unit: Literal["minute", "mile", "km"]

class Origin(BaseModel):
    lat: confloat(ge=-90, le=90)
    lon: confloat(ge=-180, le=180)

# Simplified models for API compatibility (without complex constraints)
class SimpleDistance(BaseModel):
    type: str
    value: int
    unit: str

class SimpleRestaurantQuery(BaseModel):
    location_text: Optional[str] = None
    distance: Optional[SimpleDistance] = None
    cuisines: List[str] = []
    price_tier: Optional[int] = None
    min_rating: Optional[float] = None
    open_now: Optional[bool] = None

# What your app uses after geocoding
# class ResolvedRestaurantQuery(SimpleRestaurantQuery):
#     origin: Origin | None = None         # filled by geocoder or device GPS