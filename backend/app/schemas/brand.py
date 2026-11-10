"""Brand schemas for request and response validation."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BrandCreate(BaseModel):
    brand_name: str
    description: Optional[str] = None
    industry: Optional[str] = None
    target_audience: Optional[str] = None
    objectives: Optional[str] = None
    brand_voice: Optional[str] = None

class BrandUpdate(BaseModel):
    brand_name: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    target_audience: Optional[str] = None
    objectives: Optional[str] = None
    brand_voice: Optional[str] = None

class BrandResponse(BaseModel):
    id: int
    user_id: int
    brand_name: str
    description: Optional[str]
    industry: Optional[str]
    target_audience: Optional[str]
    objectives: Optional[str]
    brand_voice: Optional[str]
    hindsight_bank_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

