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
        "start_date": goal.start_date,
        "end_date": goal.end_date
    }


def register_caloric_goal_routes(app):
    """Register all caloric goal routes."""
    from routes import caloric_goal_tag

    @app.get('/caloric-goals/current', tags=[caloric_goal_tag], responses={"200": CurrentCaloricGoalSchema, "404": ErrorSchema})
    def get_current_goal():  # noqa
        """Get the current active caloric goal value."""
        session = Session()
        try:
            today = date.today()
            goal = session.query(CaloricGoal).filter(
                CaloricGoal.end_date >= today
            ).first()

            if not goal:
                return {"message": "No active caloric goal found"}, 404

            return CurrentCaloricGoalSchema(value=goal.value).model_dump()
        finally:
            session.close()

    @app.post('/caloric-goals', tags=[caloric_goal_tag], responses={"201": CreateCaloricGoalSchema, "400": ErrorSchema})
    def create_caloric_goal(body: CreateCaloricGoalSchema):  # noqa
        """Create a new caloric goal."""
        session = Session()
        try:
            today = date.today()

            # Get the current active goal
            current_goal = session.query(CaloricGoal).filter(
                CaloricGoal.end_date >= today
            ).first()

            if current_goal:
                # If there's a goal for today, update it
                if current_goal.start_date == today:
                    current_goal.value = body.value
                    current_goal.start_date = today
                    current_goal.end_date = None  # Reset end_date to None
                    session.commit()
                    session.refresh(current_goal)
                    goal_dict = convert_caloric_goal_to_dict(current_goal)
                    return CaloricGoalSchema.model_validate(goal_dict).model_dump(), 201

                # If there's at least 1 day difference, end the current goal
                days_diff = (today - current_goal.start_date).days
                if days_diff >= 1:
                    current_goal.end_date = today
                    session.commit()
                else:
                    return {"message": "Cannot end current goal. Must wait at least 1 day from start date."}, 400

            # Create new goal
            new_goal = CaloricGoal(
                value=body.value,
                start_date=today,
                end_date=None  # New goals start with no end date
            )

            session.add(new_goal)
            session.commit()
            session.refresh(new_goal)
            goal_dict = convert_caloric_goal_to_dict(new_goal)
            return CaloricGoalSchema.model_validate(goal_dict).model_dump(), 201
        finally:
            session.close()
