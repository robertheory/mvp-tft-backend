from flask_openapi3 import Tag
from model import Session
from model.goal import Goal
from schemas.goal import GoalSchema, ListGoalSchema
from schemas.error import ErrorSchema


def convert_goal_to_dict(goal):
    """Convert a goal object to a dictionary."""
    return {
        "id": goal.id,
        "name": goal.name,
        "rate": goal.rate
    }


def register_goal_routes(app):
    """Register goal routes."""
    from routes import goal_tag

    @app.get('/goals', tags=[goal_tag], responses={"200": ListGoalSchema, "404": ErrorSchema})
    def list_goals():  # noqa
        """List all available goals."""
        session = Session()
        try:
            goals = session.query(Goal).all()
            if not goals:
                return {"message": "No goals found"}, 404

            return ListGoalSchema(
                root=[convert_goal_to_dict(goal) for goal in goals]
            ).model_dump()
        finally:
            session.close()
