from pydantic import BaseModel
from typing import List, Optional

class LocationOut(BaseModel):
    id: int
    address: Optional[str] = None
    postcode: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None

    class Config:
        from_attributes = True

class ProviderOut(BaseModel):
    id: int
    name: str
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    summary: Optional[str] = None
    locations: List[LocationOut] = []

    class Config:
        from_attributes = True
