from flask_openapi3 import Tag
from model import Session
from model.food import Food
from schemas.food import FoodSchema, ListFoodSchema
from schemas.error import ErrorSchema


# Tags
food_tag = Tag(
    name='Food',
    description='Operations for managing food'
)


def convert_food_to_dict(food):
    """Convert a food object to a dictionary."""
    return {
        "id": food.id,
        "name": food.name,
        "unit": food.unit,
        "calories": food.calories
    }


def register_food_routes(app):
    """Register food routes."""
    @app.get('/foods', tags=[food_tag], responses={"200": ListFoodSchema, "404": ErrorSchema})
    def list_foods():  # noqa
        """List all available foods."""
        session = Session()
        try:
            foods = session.query(Food).all()
            if not foods:
                return {"message": "No foods found"}, 404

            return ListFoodSchema(
                root=[convert_food_to_dict(food) for food in foods]
            ).model_dump()
        finally:
            session.close()
