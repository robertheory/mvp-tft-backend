from model import Session, Food
from flask_openapi3 import Tag, Parameter
from schemas.error import ErrorSchema
from schemas.food import FoodSchema, CreateFoodSchema, UpdateFoodSchema, DeleteFoodSchema, ListFoodSchema, GetFoodSchema
from routes import app
from pydantic import BaseModel, Field

food_tag = Tag(name="Food", description="Food operations")


class FoodPath(BaseModel):
    food_id: str = Field(..., description="Food ID",
                         example="f0dc437c-cddc-49fb-8d52-6d15e44ba6cc")


@app.get('/foods', tags=[food_tag], responses={"200": ListFoodSchema, "404": ErrorSchema})
def get_foods():
    """List all foods.
    """
    session = Session()
    foods = session.query(Food).all()
    session.close()

    return ListFoodSchema(foods=foods).model_dump()


@app.get('/foods/<food_id>', tags=[food_tag], responses={"200": GetFoodSchema, "404": ErrorSchema})
def get_food(path: FoodPath):
    """Get a food by id.
    """
    session = Session()
    food = session.query(Food).filter(Food.id == path.food_id).first()
    session.close()
    if food:
        return FoodSchema.model_validate(food).model_dump()
    return {"message": "Food not found"}, 404


@app.post('/foods', tags=[food_tag], responses={"201": CreateFoodSchema, "400": ErrorSchema})
def create_food(body: CreateFoodSchema):
    """Create a new food item.
    """
    session = Session()
    food = Food(name=body.name, unit=body.unit, calories=body.calories)
    session.add(food)
    session.commit()
    session.refresh(food)
    session.close()
    return FoodSchema.model_validate(food).model_dump(), 201


@app.put('/foods/<food_id>', tags=[food_tag], responses={"200": UpdateFoodSchema, "400": ErrorSchema})
def update_food(path: FoodPath, body: UpdateFoodSchema):
    """Update an existing food item.
    """
    session = Session()
    food = session.query(Food).filter(Food.id == path.food_id).first()
    if not food:
        return {"message": "Food not found"}, 404
    if body.name:
        food.name = body.name
    if body.unit:
        food.unit = body.unit
    if body.calories:
        food.calories = body.calories
    session.commit()
    session.refresh(food)
    session.close()
    return FoodSchema.model_validate(food).model_dump()


@app.delete('/foods/<food_id>', tags=[food_tag], responses={"200": DeleteFoodSchema, "404": ErrorSchema})
def delete_food(path: FoodPath):
    """Delete a food item.
    """
    session = Session()
    food = session.query(Food).filter(Food.id == path.food_id).first()
    if not food:
        return {"message": "Food not found"}, 404
    session.delete(food)
    session.commit()
    session.close()
    return {"message": "Food deleted"}, 200
