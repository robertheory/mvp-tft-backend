from pydantic import BaseModel, Field
from schemas.food import FoodSchema


class MealFoodSchema(BaseModel):
    """ Define how to return data from meal-food relationship.
    """
    food: FoodSchema = Field()
    quantity: int = Field(example=1)

    class Config:
        from_attributes = True
