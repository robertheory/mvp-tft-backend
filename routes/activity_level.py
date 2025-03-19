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
        "start_date": activity_level.start_date,
        "end_date": activity_level.end_date
    }


def register_activity_level_routes(app):
    """Register all activity level routes."""
    from routes import activity_level_tag

    @app.get('/activity-levels/current', tags=[activity_level_tag], responses={"200": CurrentActivityLevelSchema, "404": ErrorSchema})
    def get_current_activity_level():  # noqa
        """Get the current activity level."""
        session = Session()
        try:
            # Get the active activity level (not ended)
            activity_level = session.query(ActivityLevel).filter(
                ActivityLevel.end_date.is_(None)
            ).first()

            if not activity_level:
                return {"message": "No active activity level found"}, 404

            return CurrentActivityLevelSchema(level=activity_level.level).model_dump()
        finally:
            session.close()

    @app.post('/activity-levels', tags=[activity_level_tag], responses={"201": CreateActivityLevelSchema, "400": ErrorSchema, "404": ErrorSchema})
    def create_activity_level(body: CreateActivityLevelSchema):  # noqa
        """Create a new activity level."""
        session = Session()
        try:
            today = date.today()

            # Check if there's already an activity level for today
            existing_activity_level = session.query(ActivityLevel).filter(
                ActivityLevel.start_date == today
            ).first()

            if existing_activity_level:
                # Update existing activity level
                existing_activity_level.level = body.level
                session.commit()
                session.refresh(existing_activity_level)
                activity_level_dict = convert_activity_level_to_dict(
                    existing_activity_level)
                return ActivityLevelSchema.model_validate(activity_level_dict).model_dump(), 201

            # Check if there's an active activity level from previous days
            active_activity_level = session.query(ActivityLevel).filter(
                ActivityLevel.end_date.is_(None)
            ).first()

            if active_activity_level:
                # End the previous activity level
                active_activity_level.end_date = today
                session.commit()

            # Create new activity level
            new_activity_level = ActivityLevel(
                level=body.level,
                start_date=today
            )

            session.add(new_activity_level)
            session.commit()
            session.refresh(new_activity_level)
            activity_level_dict = convert_activity_level_to_dict(
                new_activity_level)
            return ActivityLevelSchema.model_validate(activity_level_dict).model_dump(), 201
        finally:
            session.close()
