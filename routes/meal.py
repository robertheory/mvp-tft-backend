from model import Session, Meal, Food
from flask_openapi3 import Tag
from model.meal_food import MealFood
from schemas.error import ErrorSchema
from schemas.meal import MealSchema, CreateMealSchema, UpdateMealSchema, DeleteMealSchema, ListMealSchema
from routes import app
from pydantic import BaseModel, Field

meal_tag = Tag(name="Meals", description="Meal operations")


class MealPath(BaseModel):
    meal_id: str = Field(..., description="Meal ID",
                         example="f0dc437c-cddc-49fb-8d52-6d15e44ba6cc")


@app.get('/meals', tags=[meal_tag], responses={"200": ListMealSchema, "404": ErrorSchema})
def get_meals():
    """List all meals.
    """
    session = Session()
    meals = session.query(Meal).all()
    meals_data = [MealSchema.model_validate(
        meal).model_dump() for meal in meals]
    session.close()

    return ListMealSchema(meals=meals_data).model_dump()


@app.get('/meals/<meal_id>', tags=[meal_tag], responses={"200": MealSchema, "404": ErrorSchema})
def get_meal(path: MealPath):
    """Get a meal by id.
    """
    session = Session()
    meal = session.query(Meal).filter(Meal.id == path.meal_id).first()
    if meal:
        meal_data = MealSchema.model_validate(meal).model_dump()
        session.close()
        return meal_data
    session.close()
    return {"message": "Meal not found"}, 404


@app.post('/meals', tags=[meal_tag], responses={"201": CreateMealSchema, "400": ErrorSchema})
def create_meal(body: CreateMealSchema):
    """Create a new meal.
    """
    session = Session()
    meal = Meal(title=body.title, date=body.date)
    session.add(meal)
    session.commit()
    session.refresh(meal)
    meal_data = MealSchema.model_validate(meal).model_dump()
    session.close()
    return meal_data, 201


@app.put('/meals/<meal_id>', tags=[meal_tag], responses={"200": UpdateMealSchema, "404": ErrorSchema})
def update_meal(path: MealPath, body: UpdateMealSchema):
    """Update a meal.
    """
    session = Session()
    meal = session.query(Meal).filter(Meal.id == path.meal_id).first()
    if not meal:
        session.close()
        return {"message": "Meal not found"}, 404

    if body.title:
        meal.title = body.title

    if body.date:
        meal.date = body.date

    if body.foods:
        request_foods = [item['id'] for item in body.foods]
        meal_foods = session.query(MealFood).filter(
            MealFood.meal_id == meal.id).all()
        for meal_food in meal_foods:
            if meal_food.food_id not in request_foods:
                session.delete(meal_food)
            else:
                meal_food.quantity = [
                    item['quantity'] for item in body.foods if item['id'] == meal_food.food_id][0]
        for food_id in request_foods:
            if food_id not in [meal_food.food_id for meal_food in meal_foods]:
                meal_foods.append(MealFood(
                    meal_id=meal.id, food_id=food_id, quantity=[item['quantity'] for item in body.foods if item['id'] == food_id][0]))
        meal.meal_foods = meal_foods

    session.commit()
    meal_data = MealSchema.model_validate(meal).model_dump()
    session.close()
    return meal_data


@app.delete('/meals/<meal_id>', tags=[meal_tag], responses={"200": DeleteMealSchema, "404": ErrorSchema})
def delete_meal(path: MealPath):
    """Delete a meal.
    """
    session = Session()
    meal = session.query(Meal).filter(Meal.id == path.meal_id).first()
    if not meal:
        session.close()
        return {"message": "Meal not found"}, 404
    session.delete(meal)
    session.commit()
    session.close()
    return {"message": "Meal deleted"}
