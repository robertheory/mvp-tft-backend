from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, Field, RootModel
from typing import Optional, List


class FoodSchema(BaseModel):
    """Schema for Food response."""
    id: str = Field(..., description="Food ID")
    name: str = Field(..., description="Food name")
    unit: str = Field(..., description="Food unit (e.g., grams, pieces)")
    calories: float = Field(..., description="Calories per unit", ge=0)

    class Config:
        from_attributes = True


class ListFoodSchema(RootModel):
    """Schema for list of Food responses."""
    root: List[FoodSchema] = Field(..., description="List of foods")


class DeleteFoodSchema(BaseModel):
    """Schema for deleting a food item."""
    id: str = Field(default_factory=lambda: uuid4().hex)
