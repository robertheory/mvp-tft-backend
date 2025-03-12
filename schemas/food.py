from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class FoodSchema(BaseModel):
    """ Define how a food item will be returned.
    """
    id: str
    name: str
    unit: str
    calories: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CreateFoodSchema(BaseModel):
    """ Define the schema for creating a new food item.
    """
    name: str = "Avocado"
    unit: str = "100g"
    calories: int = 160


class UpdateFoodSchema(BaseModel):
    """ Define the schema for updating an existing food item.
    """
    name: Optional[str] = "Strawberry"
    unit: Optional[str] = "50g"
    calories: Optional[int] = 30


class GetFoodSchema(BaseModel):
    """ Define the schema for getting a food item.
    """
    id: str = "1"


class ListFoodSchema(BaseModel):
    """ Define how a list of food items will be returned.
    """
    foods: list[FoodSchema]

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class DeleteFoodSchema(BaseModel):
    """ Define the schema for deleting a food item.
    """
    id: str = "1"
