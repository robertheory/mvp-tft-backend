from pydantic import BaseModel, Field
from datetime import date as date_type


class WeighInBase(BaseModel):
    """Base schema for WeighIn."""
    value: float = Field(..., description="Weight value")

    class Config:
        from_attributes = True


class CreateWeighInSchema(BaseModel):
    """Schema for creating a new weight measurement."""
    value: float = Field(..., description="Weight value")

    class Config:
        from_attributes = True


class CurrentWeighInSchema(BaseModel):
    """Schema for current weight measurement response."""
    value: float = Field(..., description="Current weight value")

    class Config:
        from_attributes = True


class WeighInSchema(WeighInBase):
    """Schema for weight measurement responses."""
    id: int = Field(..., description="Weight measurement ID")
    date: date_type = Field(..., description="Date of the weight measurement")
