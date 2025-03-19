from datetime import date
from flask_openapi3 import Tag
from pydantic import BaseModel, Field
from model import Session
from model.weigh_in import WeighIn
from schemas.weigh_in import (
    WeighInSchema,
    CreateWeighInSchema,
    CurrentWeighInSchema
)
from schemas.error import ErrorSchema

# Helper Functions


def convert_weigh_in_to_dict(weigh_in):
    """Convert a weigh in object to a dictionary."""
    return {
        "id": weigh_in.id,
        "value": weigh_in.value,
        "date": weigh_in.date
    }


def register_weigh_in_routes(app):
    """Register all weigh in routes."""
    from routes import weigh_in_tag

    @app.get('/weigh-ins/current', tags=[weigh_in_tag], responses={"200": CurrentWeighInSchema, "404": ErrorSchema})
    def get_current_weigh_in():  # noqa
        """Get the current weight measurement."""
        session = Session()
        try:
            # Get the most recent weight measurement
            weigh_in = session.query(WeighIn).order_by(
                WeighIn.date.desc()).first()

            if not weigh_in:
                return {"message": "No weight measurement found"}, 404

            return CurrentWeighInSchema(value=weigh_in.value).model_dump()
        finally:
            session.close()

    @app.post('/weigh-ins', tags=[weigh_in_tag], responses={"201": CreateWeighInSchema, "400": ErrorSchema, "404": ErrorSchema})
    def create_weigh_in(body: CreateWeighInSchema):  # noqa
        """Create a new weight measurement."""
        session = Session()
        try:
            today = date.today()

            # Check if there's already a measurement for today
            existing_weigh_in = session.query(WeighIn).filter(
                WeighIn.date == today
            ).first()

            if existing_weigh_in:
                # Update existing measurement
                existing_weigh_in.value = body.value
                session.commit()
                session.refresh(existing_weigh_in)
                weigh_in_dict = convert_weigh_in_to_dict(existing_weigh_in)
                return WeighInSchema.model_validate(weigh_in_dict).model_dump(), 201

            # Create new measurement
            new_weigh_in = WeighIn(
                value=body.value,
                date=today
            )

            session.add(new_weigh_in)
            session.commit()
            session.refresh(new_weigh_in)
            weigh_in_dict = convert_weigh_in_to_dict(new_weigh_in)
            return WeighInSchema.model_validate(weigh_in_dict).model_dump(), 201
        finally:
            session.close()
