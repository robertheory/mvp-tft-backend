from flask_openapi3 import Tag
from pydantic import BaseModel, Field
from model import Session, Meal, Food
from model.meal_food import MealFood
from schemas.meal import (
    MealSchema,
    CreateMealSchema,
    UpdateMealSchema,
    DeleteMealSchema,
    ListMealSchema
)
from schemas.error import ErrorSchema

# Path Parameters


class MealPath(BaseModel):
    meal_id: str = Field(
        ...,
        description="Meal ID",
        example="f0dc437c-cddc-49fb-8d52-6d15e44ba6cc"
    )

# Helper Functions


def convert_meal_to_dict(meal):
    """Convert a meal object to a dictionary with proper food formatting."""
    return {
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


def register_meal_routes(app):
    """Register all meal routes."""
    from routes import meal_tag

    @app.get('/meals', tags=[meal_tag], responses={"200": ListMealSchema, "404": ErrorSchema})
    def get_meals():  # noqa
        """List all meals."""
        session = Session()
        try:
            meals = session.query(Meal).all()
            meals_data = [
                MealSchema.model_validate(
                    convert_meal_to_dict(meal)).model_dump()
                for meal in meals
            ]
            return ListMealSchema(meals=meals_data).model_dump()
        finally:
            session.close()

    @app.get('/meals/<meal_id>', tags=[meal_tag], responses={"200": MealSchema, "404": ErrorSchema})
    def get_meal(path: MealPath):  # noqa
        """Get a meal by id."""
        session = Session()
        try:
            meal = session.query(Meal).filter(Meal.id == path.meal_id).first()
            if not meal:
                return {"message": "Meal not found"}, 404

            meal_dict = convert_meal_to_dict(meal)
            return MealSchema.model_validate(meal_dict).model_dump()
        finally:
            session.close()

    @app.post('/meals', tags=[meal_tag], responses={"201": CreateMealSchema, "400": ErrorSchema})
    def create_meal(body: CreateMealSchema):  # noqa
        """Create a new meal."""
        session = Session()
        try:
            meal = Meal(title=body.title, date=body.date)
            session.add(meal)
            session.commit()
            session.refresh(meal)

            if body.foods:
                for food_data in body.foods:
                    food = session.query(Food).filter(
                        Food.id == food_data['id']).first()
                    if food:
                        meal.add_food(food, food_data['quantity'])
                session.commit()
                session.refresh(meal)

            meal_dict = convert_meal_to_dict(meal)
            return MealSchema.model_validate(meal_dict).model_dump(), 201
        finally:
            session.close()

    @app.put('/meals/<meal_id>', tags=[meal_tag], responses={"200": UpdateMealSchema, "404": ErrorSchema})
    def update_meal(path: MealPath, body: UpdateMealSchema):  # noqa
        """Update a meal."""
        session = Session()
        try:
            meal = session.query(Meal).filter(Meal.id == path.meal_id).first()
            if not meal:
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
                        meal_food.quantity = next(
                            (item['quantity']
                             for item in body.foods if item['id'] == meal_food.food_id),
                            meal_food.quantity
                        )

                # Add new foods
                existing_food_ids = {
                    meal_food.food_id for meal_food in meal_foods}
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

            meal_dict = convert_meal_to_dict(meal)
            return MealSchema.model_validate(meal_dict).model_dump()
        finally:
            session.close()

    @app.delete('/meals/<meal_id>', tags=[meal_tag], responses={"200": DeleteMealSchema, "404": ErrorSchema})
    def delete_meal(path: MealPath):  # noqa
        """Delete a meal."""
        session = Session()
        try:
            meal = session.query(Meal).filter(Meal.id == path.meal_id).first()
            if not meal:
                return {"message": "Meal not found"}, 404

            session.delete(meal)
            session.commit()
            return {"message": "Meal deleted"}
        finally:
            session.close()
