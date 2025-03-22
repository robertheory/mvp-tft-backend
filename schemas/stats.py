from pydantic import BaseModel
from typing import List


class DailyCalories(BaseModel):
    """Schema for daily caloric consumption."""
    weekday: int  # Day of the week (0-6)
    value: float  # Total calories for the day


class StatsSchema(BaseModel):
    """Schema for user statistics."""
    bmr: float = 0.0  # Basal Metabolic Rate in kcal/day
    tdee: float = 0.0  # Total Daily Energy Expenditure in kcal/day
    # List of daily calories for the last 7 days
    history: List[DailyCalories] = []
