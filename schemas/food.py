from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, Field
from typing import Optional


class FoodSchema(BaseModel):
    """ Define how a food item will be returned.
    """
    id: str = Field(default_factory=lambda: uuid4().hex)
    name: str = Field(..., example="Avocado")
    unit: str = Field(..., example="100g")
    calories: int = Field(..., example=160)
    created_at: datetime = Field(..., example="2025-03-12T15:06:04.573140")
    updated_at: Optional[datetime] = Field(
        None, example="2025-03-12T15:06:04.573140")

    class Config:
        from_attributes = True


class CreateFoodSchema(BaseModel):
    """ Define the schema for creating a new food item.
    """
    name: str = Field(..., example="Avocado")
    unit: str = Field(..., example="100g")
    calories: int = Field(..., example=160)


class UpdateFoodSchema(BaseModel):
    """ Define the schema for updating an existing food item.
    """
    name: Optional[str] = Field(None, example="Strawberry")
    unit: Optional[str] = Field(None, example="50g")
    calories: Optional[int] = Field(None, example=30)


class GetFoodSchema(BaseModel):
    """ Define the schema for getting a food item.
    """
    id: str = Field(default_factory=lambda: uuid4().hex)


class ListFoodSchema(BaseModel):
    """ Define how a list of food items will be returned.
    """
    foods: list[FoodSchema] = Field(..., example=[
        {
            "id": "f0dc437c-cddc-49fb-8d52-6d15e44ba6cc",
            "name": "Avocado",
            "unit": "100g",
            "calories": 160,
            "created_at": "2025-03-12T15:06:04.573140",
            "updated_at": "2025-03-12T15:06:04.573140"
        },
        {
            "id": "f0dc437c-cddc-49fb-8d52-6d15e44ba6cc",
            "name": "Strawberry",
            "unit": "50g",
            "calories": 30,
            "created_at": "2025-03-12T15:06:04.573140",
            "updated_at": "2025-03-12T15:06:04.573140"
        }])


class DeleteFoodSchema(BaseModel):
    """ Define the schema for deleting a food item.
    """
    id: str = Field(default_factory=lambda: uuid4().hex)
