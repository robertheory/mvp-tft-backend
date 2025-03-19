from datetime import date, datetime
from flask_openapi3 import Tag
from pydantic import BaseModel, Field
from model import Session
from model.personal_info import PersonalInfo
from schemas.personal_info import (
    PersonalInfoSchema,
    CreatePersonalInfoSchema,
    CurrentPersonalInfoSchema
)
from schemas.error import ErrorSchema

# Tags
personal_info_tag = Tag(
    name='Personal Info',
    description='Operations for managing personal information'
)

# Helper Functions


def convert_personal_info_to_dict(personal_info):
    """Convert a personal info object to a dictionary."""
    return {
        "id": personal_info.id,
        "age": personal_info.age,
        "gender": personal_info.gender,
        "height": personal_info.height,
        "weight": personal_info.weight,
        "goal_id": personal_info.goal_id,
        "activity_level_id": personal_info.activity_level_id,
        "date": personal_info.date
    }


def register_personal_info_routes(app):
    """Register all personal info routes."""
    @app.get('/personal-info/current', tags=[personal_info_tag], responses={"200": CurrentPersonalInfoSchema, "404": ErrorSchema})
    def get_current_personal_info():  # noqa
        """Get the current personal info."""
        session = Session()
        try:
            # Get the most recent personal info
            personal_info = session.query(PersonalInfo).order_by(
                PersonalInfo.date.desc()).first()

            if not personal_info:
                return {"message": "No personal info found"}, 404

            return CurrentPersonalInfoSchema(
                age=personal_info.age,
                gender=personal_info.gender,
                height=personal_info.height,
                weight=personal_info.weight,
                goal_id=personal_info.goal_id,
                activity_level_id=personal_info.activity_level_id,
                date=personal_info.date
            ).model_dump()
        finally:
            session.close()

    @app.post('/personal-info', tags=[personal_info_tag], responses={"201": CreatePersonalInfoSchema, "400": ErrorSchema})
    def create_personal_info(body: CreatePersonalInfoSchema):  # noqa
        """Create a new personal info record."""
        session = Session()
        try:
            today = datetime.now()

            # Check if there's already a record for today
            existing_info = session.query(PersonalInfo).filter(
                PersonalInfo.date >= today.replace(
                    hour=0, minute=0, second=0, microsecond=0)
            ).first()

            if existing_info:
                # Update existing record
                existing_info.age = body.age
                existing_info.gender = body.gender
                existing_info.height = body.height
                existing_info.weight = body.weight
                existing_info.goal_id = body.goal_id
                existing_info.activity_level_id = body.activity_level_id
                session.commit()
                session.refresh(existing_info)
                info_dict = convert_personal_info_to_dict(existing_info)
                return PersonalInfoSchema.model_validate(info_dict).model_dump(), 201

            # Create new record
            new_info = PersonalInfo(
                age=body.age,
                gender=body.gender,
                height=body.height,
                weight=body.weight,
                goal_id=body.goal_id,
                activity_level_id=body.activity_level_id,
                date=today
            )

            session.add(new_info)
            session.commit()
            session.refresh(new_info)
            info_dict = convert_personal_info_to_dict(new_info)
            return PersonalInfoSchema.model_validate(info_dict).model_dump(), 201
        finally:
            session.close()
