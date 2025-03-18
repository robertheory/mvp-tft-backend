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
    meals_data = []
    for meal in meals:
        meal_dict = {
            "id": meal.id,
            "title": meal.title,
            "date": meal.date,
            "foods": [
                {
                    "id": meal_food.food.id,
                    "name": meal_food.food.name,
                    "unit": meal_food.food.unit,
                    "calories": meal_food.food.calories,
                    "quantity": meal_food.quantity
                }
                for meal_food in meal.meal_foods
            ]
        }
        meals_data.append(MealSchema.model_validate(meal_dict).model_dump())
    session.close()

    return ListMealSchema(meals=meals_data).model_dump()


@app.get('/meals/<meal_id>', tags=[meal_tag], responses={"200": MealSchema, "404": ErrorSchema})
def get_meal(path: MealPath):
    """Get a meal by id.
    """
    session = Session()
    meal = session.query(Meal).filter(Meal.id == path.meal_id).first()
    if meal:
        # Convert meal_foods to the expected format
        meal_dict = {
            "id": meal.id,
            "title": meal.title,
            "date": meal.date,
            "foods": [
                {
                    "id": meal_food.food.id,
                    "name": meal_food.food.name,
                    "unit": meal_food.food.unit,
                    "calories": meal_food.food.calories,
                    "quantity": meal_food.quantity
                }
                for meal_food in meal.meal_foods
            ]
        }
        meal_data = MealSchema.model_validate(meal_dict).model_dump()
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

    # Process foods if provided
    if body.foods:
        for food_data in body.foods:
            food = session.query(Food).filter(
                Food.id == food_data['id']).first()
            if food:
                meal.add_food(food, food_data['quantity'])
        session.commit()
        session.refresh(meal)

    # Convert to response format
    meal_dict = {
        "id": meal.id,
        "title": meal.title,
        "date": meal.date,
        "foods": [
            {
                "id": meal_food.food.id,
                "name": meal_food.food.name,
                "unit": meal_food.food.unit,
                "calories": meal_food.food.calories,
                "quantity": meal_food.quantity
            }
            for meal_food in meal.meal_foods
        ]
    }
    meal_data = MealSchema.model_validate(meal_dict).model_dump()
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

        # Remove foods that are not in the request
        for meal_food in meal_foods:
            if meal_food.food_id not in request_foods:
                session.delete(meal_food)
            else:
                # Update quantity for existing foods
                meal_food.quantity = next(
                    (item['quantity']
                     for item in body.foods if item['id'] == meal_food.food_id),
                    meal_food.quantity
                )

        # Add new foods
        existing_food_ids = {meal_food.food_id for meal_food in meal_foods}
        for food_data in body.foods:
            if food_data['id'] not in existing_food_ids:
                new_meal_food = MealFood(
                    meal_id=meal.id,
                    food_id=food_data['id'],
                    quantity=food_data['quantity']
                )
                session.add(new_meal_food)

        session.commit()
        session.refresh(meal)

    # Convert to response format
    meal_dict = {
        "id": meal.id,
        "title": meal.title,
        "date": meal.date,
        "foods": [
            {
                "id": meal_food.food.id,
                "name": meal_food.food.name,
                "unit": meal_food.food.unit,
                "calories": meal_food.food.calories,
                "quantity": meal_food.quantity
            }
            for meal_food in meal.meal_foods
        ]
    }
    meal_data = MealSchema.model_validate(meal_dict).model_dump()
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
