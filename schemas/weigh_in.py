from pydantic import BaseModel, Field
from datetime import date as date_type


class WeighInBase(BaseModel):
    """Base schema for WeighIn."""
    value: float = Field(..., description="Weight value in kg")
    date: date_type = Field(..., description="Date of the weight measurement")

    class Config:
        from_attributes = True


class CreateWeighInSchema(BaseModel):
    """Schema for creating a new WeighIn."""
    value: float = Field(..., description="Weight value in kg")

    class Config:
        from_attributes = True


class CurrentWeighInSchema(BaseModel):
    """Schema for current WeighIn response."""
    value: float = Field(..., description="Current weight value in kg")

    class Config:
        from_attributes = True


class WeighInSchema(WeighInBase):
    """Schema for WeighIn response."""
    id: int = Field(..., description="WeighIn ID")
