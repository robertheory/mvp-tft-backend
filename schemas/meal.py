from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, Field
from typing import Optional, List
from schemas.meal_food import MealFoodSchema


class MealSchema(BaseModel):
    """ Define how a meal will be returned.
    """
    id: str = Field(default_factory=lambda: uuid4().hex)
    title: str = Field(..., example="Lunch")
    date: datetime = Field(..., example=datetime.now().isoformat())

    meal_foods: List[MealFoodSchema] = Field(
        serialization_alias="foods")
    # foods: List[FoodSchema] = Field(alias="foods", alias_priority=2)

    class Config:
        from_attributes = True


class CreateMealSchema(BaseModel):
    """ Define the schema for creating a new meal.
    """
    title: str = Field(..., example="Lunch")
    date: datetime = Field(..., example=datetime.now().isoformat())

    foods: List[dict] = Field([], example=[
        {
            "id": "7be49f8f-bb90-4ec1-8413-744d24ace238",
            "quantity": 10
        },
        {
            "id": "f0dc437c-cddc-49fb-8d52-6d15e44ba6cc",
            "quantity": 20
        }
    ])


class UpdateMealSchema(BaseModel):
    """ Define the schema for updating an existing meal.
    """
    title: Optional[str] = Field(..., example="Lunch")
    date: Optional[datetime] = Field(..., example=datetime.now().isoformat())

    foods: Optional[List[dict]] = Field([], example=[])


class DeleteMealSchema(BaseModel):
    """ Define the schema for deleting a meal.
    """
    id: str = Field(default_factory=lambda: uuid4().hex)


class ListMealSchema(BaseModel):
    """ Define how a list of meals will be returned.
    """
    meals: List[MealSchema] = Field(..., example=[])

    class Config:
        from_attributes = True
