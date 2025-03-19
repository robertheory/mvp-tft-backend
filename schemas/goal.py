from pydantic import BaseModel, Field, RootModel


class GoalSchema(BaseModel):
    """Schema for Goal."""
    id: int = Field(..., description="Goal ID")
    name: str = Field(..., description="Name of the goal")

    class Config:
        from_attributes = True


class ListGoalSchema(RootModel):
    """Schema for list of Goal responses."""
    root: list[GoalSchema] = Field(..., description="List of goals")
