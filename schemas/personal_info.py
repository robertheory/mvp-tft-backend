from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from schemas.activity_level import ActivityLevelSchema


class PersonalInfoBase(BaseModel):
    """Base schema for PersonalInfo."""
    age: int = Field(..., description="Age in years", ge=0)
    gender: str = Field(..., description="Gender (M/F)")
    height: float = Field(..., description="Height in meters", gt=0)
    weight: float = Field(..., description="Weight in kg", gt=0)
    goal: str = Field(..., description="Fitness goal")
    activity_level_id: int = Field(..., description="ID of the activity level")
    date: datetime = Field(..., description="Date of the personal info")

    class Config:
        from_attributes = True


class CreatePersonalInfoSchema(BaseModel):
    """Schema for creating a new PersonalInfo."""
    age: int = Field(..., description="Age in years", ge=0)
    gender: str = Field(..., description="Gender (M/F)")
    height: float = Field(..., description="Height in meters", gt=0)
    weight: float = Field(..., description="Weight in kg", gt=0)
    goal: str = Field(..., description="Fitness goal")
    activity_level_id: int = Field(..., description="ID of the activity level")

    class Config:
        from_attributes = True


class CurrentPersonalInfoSchema(BaseModel):
    """Schema for current PersonalInfo response."""
    age: int = Field(..., description="Age in years")
    gender: str = Field(..., description="Gender (M/F)")
    height: float = Field(..., description="Height in meters")
    weight: float = Field(..., description="Weight in kg")
    goal: str = Field(..., description="Fitness goal")
    activity_level: ActivityLevelSchema = Field(
        ..., description="Activity level information")
    date: datetime = Field(..., description="Date of the personal info")

    class Config:
        from_attributes = True


class PersonalInfoSchema(PersonalInfoBase):
    """Schema for PersonalInfo response."""
    id: int = Field(..., description="PersonalInfo ID")
    activity_level: ActivityLevelSchema = Field(
        ..., description="Activity level information")


class ListPersonalInfoSchema(BaseModel):
    """Schema for list of PersonalInfo responses."""
    personal_infos: list[PersonalInfoSchema] = Field(
        ..., description="List of personal info records")
