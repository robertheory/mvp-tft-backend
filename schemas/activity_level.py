from pydantic import BaseModel, Field, RootModel


class ActivityLevelBase(BaseModel):
    """Base schema for ActivityLevel."""
    name: str = Field(..., description="Name of the activity level")
    description: str = Field(...,
                             description="Description of the activity level")
    multiplier: float = Field(
        ..., description="Multiplier for this activity level")

    class Config:
        from_attributes = True


class ActivityLevelSchema(BaseModel):
    """Schema for ActivityLevel."""
    id: int = Field(..., description="Activity Level ID")
    name: str = Field(..., description="Name of the activity level")
    description: str = Field(...,
                             description="Description of the activity level")

    class Config:
        from_attributes = True


class ListActivityLevelSchema(RootModel):
    """Schema for list of ActivityLevel responses."""
    root: list[ActivityLevelSchema] = Field(...,
                                            description="List of activity levels")
