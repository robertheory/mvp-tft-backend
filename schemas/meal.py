from pydantic import BaseModel
from typing import Optional, List
from schemas.food import FoodSchema


class MealCreateSchema(BaseModel):
    """ Define the schema for creating a new meal.
    """
    title: str = "Breakfast"
    date: str = "2021-01-01T00:00:00Z"

    foods: Optional[List[dict]] = []


class MealUpdateSchema(BaseModel):
    """ Define the schema for updating an existing meal.
    """
    title: Optional[str] = "Lunch"
    date: Optional[str] = "2021-01-01T00:00:00Z"

    foods: Optional[List[dict]] = []


class MealDeleteSchema(BaseModel):
    """ Define the schema for deleting a meal.
    """
    id: str


class MealSchema(BaseModel):
    """ Define how a meal will be returned.
    """
    id: str
    title: str
    date: str

    foods: List[dict]

    class Config:
        from_attributes = True


class ListMealSchema(BaseModel):
    """ Define how a list of meals will be returned.
    """
    meals: List[MealSchema]

    class Config:
        from_attributes = True
