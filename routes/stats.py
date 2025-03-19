from flask_openapi3 import Tag
from model import Session
from model.personal_info import PersonalInfo
from model.activity_level import ActivityLevel
from model.goal import Goal
from schemas.stats import StatsSchema
from schemas.error import ErrorSchema


# Tags
stats_tag = Tag(
    name='Stats',
    description='Operations for getting user statistics'
)


def calculate_bmr(gender: str, weight: float, height: float, age: int) -> float:
    """
    Calculates the Basal Metabolic Rate (BMR) using the Harris-Benedict formula.

    Parameters:
    - gender (str): 'M' or 'F'
    - weight (float): weight in kg
    - height (float): height in cm
    - age (int): age in years

    Returns:
    - bmr (float): Basal Metabolic Rate in kcal/day
    """
    if gender.lower() == 'm':
        bmr = 66.5 + (13.75 * weight) + (5 * height) - (6.75 * age)
    elif gender.lower() == 'f':
        bmr = 655.1 + (9.56 * weight) + (1.85 * height) - (4.68 * age)
    else:
        raise ValueError("Invalid gender. Use 'M' or 'F'.")

    return bmr


def calculate_tdee(bmr: float, multiplier: float, goal_rate: float) -> float:
    """
    Calculates the Total Daily Energy Expenditure (TDEE) based on BMR, activity level, and goal rate.

    Parameters:
    - bmr (float): Basal Metabolic Rate in kcal/day
    - multiplier (float): 1.2, 1.375, 1.55, 1.725, 1.9
    - goal_rate (float): -0.2, -0.1, 0, 0.1, 0.2

    Returns:
    - tdee (float): Total Daily Energy Expenditure in kcal/day
    """

    # Calculate TDEE
    tdee = bmr * multiplier

    # Adjust TDEE based on goal rate
    tdee = tdee + (tdee * goal_rate)

    return tdee


def register_stats_routes(app):
    """Register stats routes."""
    @app.get('/stats', tags=[stats_tag], responses={"200": StatsSchema, "404": ErrorSchema})
    def get_stats():  # noqa
        """Get user statistics including BMR and TDEE."""
        session = Session()
        try:
            # Get the most recent personal info
            personal_info = session.query(PersonalInfo).order_by(
                PersonalInfo.date.desc()
            ).first()

            if not personal_info:
                return {"message": "No personal info found"}, 404

            # Get activity level and goal
            activity_level = session.query(ActivityLevel).filter(
                ActivityLevel.id == personal_info.activity_level_id
            ).first()

            goal = session.query(Goal).filter(
                Goal.id == personal_info.goal_id
            ).first()

            if not activity_level or not goal:
                return {"message": "Activity level or goal not found"}, 404

            # Calculate BMR
            bmr = calculate_bmr(
                gender=personal_info.gender,
                weight=personal_info.weight,
                height=personal_info.height,
                age=personal_info.age
            )

            # Calculate TDEE
            tdee = calculate_tdee(
                bmr=bmr,
                multiplier=activity_level.multiplier,
                goal_rate=goal.rate
            )

            return StatsSchema(
                bmr=round(bmr, 2),
                tdee=round(tdee, 2)
            ).model_dump()
        finally:
            session.close()
