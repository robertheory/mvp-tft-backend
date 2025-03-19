from pydantic import BaseModel, Field


class GoalSchema(BaseModel):
    """Schema for Goal."""
    id: int = Field(..., description="Goal ID")
    name: str = Field(..., description="Name of the goal")
    rate: float = Field(..., description="Rate of weight change per week")

    class Config:
        from_attributes = True
