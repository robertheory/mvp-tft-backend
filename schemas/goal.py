from pydantic import BaseModel, Field, RootModel
from typing import List


class GoalSchema(BaseModel):
    """Schema for Goal response."""
    id: int = Field(..., description="Goal ID")
    name: str = Field(..., description="Goal name")
    rate: float = Field(
        ..., description="Weight change rate per week (positive for gain, negative for loss)")

    class Config:
        from_attributes = True


class ListGoalSchema(RootModel):
    """Schema for list of Goal responses."""
    root: List[GoalSchema] = Field(..., description="List of goals")

    class Config:
        from_attributes = True
