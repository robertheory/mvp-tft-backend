from flask_openapi3 import Tag
from model import Session
from model.activity_level import ActivityLevel
from schemas.activity_level import ListActivityLevelSchema
from schemas.error import ErrorSchema


def register_activity_level_routes(app):
    """Register all activity level routes."""
    from routes import activity_level_tag

    @app.get('/activity-levels', tags=[activity_level_tag], responses={"200": ListActivityLevelSchema, "404": ErrorSchema})
    def list_activity_levels():  # noqa
        """List all activity levels."""
        session = Session()
        try:
            activity_levels = session.query(ActivityLevel).all()
            if not activity_levels:
                return {"message": "No activity levels found"}, 404

            return ListActivityLevelSchema(root=activity_levels).model_dump()
        finally:
            session.close()
