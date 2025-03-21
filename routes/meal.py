from flask_openapi3 import Tag
from pydantic import BaseModel, Field
from model import Session
from model.meal import Meal
from model.meal_food import MealFood
from model.food import Food
from schemas.meal import (
    MealSchema,
    CreateMealSchema,
    ListMealSchema,
    UpdateMealSchema
)
from schemas.error import ErrorSchema

# Tags
meal_tag = Tag(
    name='Meals',
    description='Operations for managing meals'
)

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
        "date": meal.date.replace(microsecond=0).isoformat(),
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
    @app.post('/meals', tags=[meal_tag], responses={"201": CreateMealSchema, "400": ErrorSchema})
    def create_meal(body: CreateMealSchema):  # noqa
        """Create a new meal."""
        session = Session()
        try:
            # Create new meal
            new_meal = Meal(
                title=body.title,
                date=body.date
            )
            session.add(new_meal)
            session.commit()

            # Add food relationships
            for food_data in body.foods:
                food = session.query(Food).filter(
                    Food.id == food_data["id"]).first()
                if not food:
                    return {"message": f"Food with id {food_data['id']} not found"}, 404

                meal_food = MealFood(
                    meal_id=new_meal.id,
                    food_id=food_data["id"],
                    quantity=food_data["quantity"]
                )
                session.add(meal_food)

            session.commit()
            session.refresh(new_meal)
            meal_dict = convert_meal_to_dict(new_meal)
            return MealSchema.model_validate(meal_dict).model_dump(), 201
        finally:
            session.close()

    @app.get('/meals', tags=[meal_tag], responses={"200": ListMealSchema, "404": ErrorSchema})
    def list_meals():  # noqa
        """List all meals."""
        session = Session()
        try:
            # Join with Food table to ensure we have food data
            meals = session.query(Meal).join(MealFood).join(Food).all()
            if not meals:
                return []

            return ListMealSchema(
                root=[convert_meal_to_dict(meal) for meal in meals]
            ).model_dump()
        finally:
            session.close()

    @app.get('/meals/<meal_id>', tags=[meal_tag], responses={"200": MealSchema, "404": ErrorSchema})
    def get_meal(path: MealPath):  # noqa
        """Get a meal by ID."""
        session = Session()
        try:
            # Join with Food table to ensure we have food data
            meal = session.query(Meal).join(MealFood).join(
                Food).filter(Meal.id == path.meal_id).first()
            if not meal:
                return {"message": "Meal not found"}, 404

            meal_dict = convert_meal_to_dict(meal)
            return MealSchema.model_validate(meal_dict).model_dump()
        finally:
            session.close()

    @app.put('/meals/<meal_id>', tags=[meal_tag], responses={"200": MealSchema, "404": ErrorSchema})
    def update_meal(path: MealPath, body: UpdateMealSchema):  # noqa
        """Update a meal."""
        session = Session()
        try:
            meal = session.query(Meal).filter(Meal.id == path.meal_id).first()
            if not meal:
                return {"message": "Meal not found"}, 404

            if body.title is not None:
                meal.title = body.title
            if body.date is not None:
                meal.date = body.date

            if body.foods is not None:
                # Remove existing food relationships
                session.query(MealFood).filter(
                    MealFood.meal_id == path.meal_id).delete()

                # Add new food relationships
                for food_data in body.foods:
                    food = session.query(Food).filter(
                        Food.id == food_data["id"]).first()
                    if not food:
                        return {"message": f"Food with id {food_data['id']} not found"}, 404

                    meal_food = MealFood(
                        meal_id=path.meal_id,
                        food_id=food_data["id"],
                        quantity=food_data["quantity"]
                    )
                    session.add(meal_food)

            session.commit()
            session.refresh(meal)
            meal_dict = convert_meal_to_dict(meal)
            return MealSchema.model_validate(meal_dict).model_dump()
        finally:
            session.close()

    @app.delete('/meals/<meal_id>', tags=[meal_tag], responses={"204": None, "404": ErrorSchema})
    def delete_meal(path: MealPath):  # noqa
        """Delete a meal."""
        session = Session()
        try:
            meal = session.query(Meal).filter(Meal.id == path.meal_id).first()
            if not meal:
                return {"message": "Meal not found"}, 404

            # Delete meal food relationships first
            session.query(MealFood).filter(
                MealFood.meal_id == path.meal_id).delete()
            session.delete(meal)
            session.commit()
            return "", 204
        finally:
            session.close()
