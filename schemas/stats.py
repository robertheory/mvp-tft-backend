from pydantic import BaseModel


class StatsSchema(BaseModel):
    """Schema for user statistics."""
    bmr: float = 0.0  # Basal Metabolic Rate in kcal/day
    tdee: float = 0.0  # Total Daily Energy Expenditure in kcal/day
