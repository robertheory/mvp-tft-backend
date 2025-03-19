from pydantic import BaseModel, Field
from datetime import date as date_type


class CaloricGoalBase(BaseModel):
    """Base schema for CaloricGoal."""
    value: float = Field(..., description="Caloric goal value")
    date: date_type = Field(..., description="Date of the caloric goal")

    class Config:
        from_attributes = True


class CreateCaloricGoalSchema(BaseModel):
    """Schema for creating a new CaloricGoal."""
    value: float = Field(..., description="Caloric goal value")

    class Config:
        from_attributes = True


class CurrentCaloricGoalSchema(BaseModel):
    """Schema for current CaloricGoal response."""
    value: float = Field(..., description="Current caloric goal value")

    class Config:
        from_attributes = True


class CaloricGoalSchema(CaloricGoalBase):
    """Schema for CaloricGoal response."""
    id: int = Field(..., description="CaloricGoal ID")
