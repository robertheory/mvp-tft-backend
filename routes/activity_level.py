from datetime import date
from flask_openapi3 import Tag
from pydantic import BaseModel, Field
from model import Session
from model.activity_level import ActivityLevel
from schemas.activity_level import (
    ActivityLevelSchema,
    CreateActivityLevelSchema,
    CurrentActivityLevelSchema
)
from schemas.error import ErrorSchema

# Helper Functions


def convert_activity_level_to_dict(activity_level):
    """Convert an activity level object to a dictionary."""
    return {
        "id": activity_level.id,
        "level": activity_level.level,
        "date": activity_level.date
    }


def register_activity_level_routes(app):
    """Register all activity level routes."""
    from routes import activity_level_tag

    @app.get('/activity-levels/current', tags=[activity_level_tag], responses={"200": CurrentActivityLevelSchema, "404": ErrorSchema})
    def get_current_activity_level():  # noqa
        """Get the current activity level."""
        session = Session()
        try:
            # Get the most recent activity level
            activity_level = session.query(ActivityLevel).order_by(
                ActivityLevel.date.desc()).first()

            if not activity_level:
                return {"message": "No activity level found"}, 404

            return CurrentActivityLevelSchema(level=activity_level.level).model_dump()
        finally:
            session.close()

    @app.post('/activity-levels', tags=[activity_level_tag], responses={"201": CreateActivityLevelSchema, "400": ErrorSchema})
    def create_activity_level(body: CreateActivityLevelSchema):  # noqa
        """Create a new activity level."""
        session = Session()
        try:
            today = date.today()

            # Check if there's already a level for today
            existing_level = session.query(ActivityLevel).filter(
                ActivityLevel.date == today
            ).first()

            if existing_level:
                # Update existing level
                existing_level.level = body.level
                session.commit()
                session.refresh(existing_level)
                level_dict = convert_activity_level_to_dict(existing_level)
                return ActivityLevelSchema.model_validate(level_dict).model_dump(), 201

            # Create new level
            new_level = ActivityLevel(
                level=body.level,
                date=today
            )

            session.add(new_level)
            session.commit()
            session.refresh(new_level)
            level_dict = convert_activity_level_to_dict(new_level)
            return ActivityLevelSchema.model_validate(level_dict).model_dump(), 201
        finally:
            session.close()
