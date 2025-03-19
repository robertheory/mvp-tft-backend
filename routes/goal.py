from flask_openapi3 import Tag
from model import Session
from model.goal import Goal
from schemas.goal import ListGoalSchema
from schemas.error import ErrorSchema


def register_goal_routes(app):
    """Register all goal routes."""
    from routes import goal_tag

    @app.get('/goals', tags=[goal_tag], responses={"200": ListGoalSchema, "404": ErrorSchema})
    def list_goals():  # noqa
        """List all goals."""
        session = Session()
        try:
            goals = session.query(Goal).all()
            if not goals:
                return {"message": "No goals found"}, 404

            return ListGoalSchema(root=goals).model_dump()
        finally:
            session.close()
