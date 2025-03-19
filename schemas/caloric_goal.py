from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class CaloricGoalBase(BaseModel):
    """Base schema for CaloricGoal."""
    value: float = Field(..., description="Daily caloric goal value")
    start_date: date = Field(..., description="Start date of the caloric goal")
    end_date: Optional[date] = Field(
        None, description="End date of the caloric goal")


class CreateCaloricGoalSchema(BaseModel):
    """Schema for creating a new caloric goal."""
    value: float = Field(..., description="Daily caloric goal value")


class CurrentCaloricGoalSchema(BaseModel):
    """Schema for current caloric goal response."""
    value: float = Field(..., description="Current daily caloric goal value")


class CaloricGoalSchema(CaloricGoalBase):
    """Schema for caloric goal responses."""
    id: int = Field(..., description="Caloric goal ID")

    class Config:
        from_attributes = True
