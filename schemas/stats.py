from pydantic import BaseModel, RootModel
from typing import List


class DailyCalories(BaseModel):
    """Schema for daily caloric consumption."""
    date: str  # Date in format MM/DD
    value: float  # Total calories for the day


class RatesSchema(BaseModel):
    """Schema for user statistics."""
    bmr: float = 0.0  # Basal Metabolic Rate in kcal/day
    tdee: float = 0.0  # Total Daily Energy Expenditure in kcal/day


class HistorySchema(RootModel):
    """Schema for user's caloric history."""
    root: List[DailyCalories] = []
