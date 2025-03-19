from datetime import date
from flask_openapi3 import Tag
from pydantic import BaseModel, Field
from model import Session
from model.caloric_goal import CaloricGoal
from schemas.caloric_goal import (
    CaloricGoalSchema,
    CreateCaloricGoalSchema,
    CurrentCaloricGoalSchema
)
from schemas.error import ErrorSchema

# Helper Functions


def convert_caloric_goal_to_dict(goal):
    """Convert a caloric goal object to a dictionary."""
    return {
        "id": goal.id,
        "value": goal.value,
        "date": goal.date
    }


def register_caloric_goal_routes(app):
    """Register all caloric goal routes."""
    from routes import caloric_goal_tag

    @app.get('/caloric-goals/current', tags=[caloric_goal_tag], responses={"200": CurrentCaloricGoalSchema, "404": ErrorSchema})
    def get_current_goal():  # noqa
        """Get the current caloric goal value."""
        session = Session()
        try:
            # Get the most recent caloric goal
            goal = session.query(CaloricGoal).order_by(
                CaloricGoal.date.desc()).first()

            if not goal:
                return {"message": "No caloric goal found"}, 404

            return CurrentCaloricGoalSchema(value=goal.value).model_dump()
        finally:
            session.close()

    @app.post('/caloric-goals', tags=[caloric_goal_tag], responses={"201": CreateCaloricGoalSchema, "400": ErrorSchema})
    def create_caloric_goal(body: CreateCaloricGoalSchema):  # noqa
        """Create a new caloric goal."""
        session = Session()
        try:
            today = date.today()

            # Check if there's already a goal for today
            existing_goal = session.query(CaloricGoal).filter(
                CaloricGoal.date == today
            ).first()

            if existing_goal:
                # Update existing goal
                existing_goal.value = body.value
                session.commit()
                session.refresh(existing_goal)
                goal_dict = convert_caloric_goal_to_dict(existing_goal)
                return CaloricGoalSchema.model_validate(goal_dict).model_dump(), 201

            # Create new goal
            new_goal = CaloricGoal(
                value=body.value,
                date=today
            )

            session.add(new_goal)
            session.commit()
            session.refresh(new_goal)
            goal_dict = convert_caloric_goal_to_dict(new_goal)
            return CaloricGoalSchema.model_validate(goal_dict).model_dump(), 201
        finally:
            session.close()
