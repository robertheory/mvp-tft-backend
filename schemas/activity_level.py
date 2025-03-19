from pydantic import BaseModel, Field


class ActivityLevelBase(BaseModel):
    """Base schema for ActivityLevel."""
    name: str = Field(..., description="Name of the activity level")
    description: str = Field(...,
                             description="Description of the activity level")
    calories_per_hour: float = Field(
        ..., description="Calories burned per hour for this activity level")

    class Config:
        from_attributes = True


class ActivityLevelSchema(ActivityLevelBase):
    """Schema for ActivityLevel response."""
    id: int = Field(..., description="ActivityLevel ID")
