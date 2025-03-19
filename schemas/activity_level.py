from pydantic import BaseModel, Field
from datetime import date as date_type
from typing import Optional


class ActivityLevelBase(BaseModel):
    """Base schema for ActivityLevel."""
    level: str = Field(..., description="Activity level")
    start_date: date_type = Field(...,
                                  description="Start date of the activity level")
    end_date: Optional[date_type] = Field(
        None, description="End date of the activity level")

    class Config:
        from_attributes = True


class CreateActivityLevelSchema(BaseModel):
    """Schema for creating a new activity level."""
    level: str = Field(..., description="Activity level")

    class Config:
        from_attributes = True


class CurrentActivityLevelSchema(BaseModel):
    """Schema for current activity level response."""
    level: str = Field(..., description="Current activity level")

    class Config:
        from_attributes = True


class ActivityLevelSchema(ActivityLevelBase):
    """Schema for activity level responses."""
    id: int = Field(..., description="Activity level ID")
