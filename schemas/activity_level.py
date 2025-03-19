from pydantic import BaseModel, Field
from datetime import date as date_type


class ActivityLevelBase(BaseModel):
    """Base schema for ActivityLevel."""
    level: str = Field(..., description="Activity level")
    date: date_type = Field(..., description="Date of the activity level")

    class Config:
        from_attributes = True


class CreateActivityLevelSchema(BaseModel):
    """Schema for creating a new ActivityLevel."""
    level: str = Field(..., description="Activity level")

    class Config:
        from_attributes = True


class CurrentActivityLevelSchema(BaseModel):
    """Schema for current ActivityLevel response."""
    level: str = Field(..., description="Current activity level")

    class Config:
        from_attributes = True


class ActivityLevelSchema(ActivityLevelBase):
    """Schema for ActivityLevel response."""
    id: int = Field(..., description="ActivityLevel ID")
