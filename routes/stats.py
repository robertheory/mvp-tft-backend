from flask_openapi3 import Tag
from model import Session
from model.personal_info import PersonalInfo
from model.activity_level import ActivityLevel
from model.goal import Goal
from model.meal import Meal
from model.meal_food import MealFood
from model.food import Food
from schemas.stats import RatesSchema, HistorySchema, DailyCalories
from schemas.error import ErrorSchema
from datetime import datetime, timedelta
from sqlalchemy import func


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


def get_user_rates(session):
    """Get user's BMR and TDEE statistics."""
    # Get the most recent personal info
    personal_info = session.query(PersonalInfo).order_by(
        PersonalInfo.date.desc()
    ).first()

    if not personal_info:
        return RatesSchema(bmr=0.0, tdee=0.0), None

    # Get activity level and goal
    activity_level = session.query(ActivityLevel).filter(
        ActivityLevel.id == personal_info.activity_level_id
    ).first()

    goal = session.query(Goal).filter(
        Goal.id == personal_info.goal_id
    ).first()

    if not activity_level or not goal:
        return RatesSchema(bmr=0.0, tdee=0.0), None

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

    return RatesSchema(
        bmr=round(bmr, 2),
        tdee=round(tdee, 2)
    ), None


def get_user_history(session):
    """Get user's caloric history for the last 7 days."""
    # Get last 7 days of meals
    end_date = datetime.now()
    # Set end_date to midnight of tomorrow to include all of today's meals
    end_date = end_date.replace(
        hour=23, minute=59, second=59, microsecond=999999)
    # Set start_date to midnight of 6 days ago
    start_date = (end_date - timedelta(days=6)
                  ).replace(hour=0, minute=0, second=0, microsecond=0)

    history = []

    meals = session.query(Meal).join(MealFood).join(Food).filter(
        Meal.date >= start_date, Meal.date <= end_date).all()

    for meal in meals:
        meal_calories = 0
        for meal_food in meal.meal_foods:
            meal_calories += meal_food.food.calories * meal_food.quantity

        history.append(DailyCalories(
            date=meal.date.strftime("%Y-%m-%d"),
            value=meal_calories
        ))

    return HistorySchema(root=history)


def register_stats_routes(app):
    """Register stats routes."""
    @app.get('/stats/rates', tags=[stats_tag], responses={"200": RatesSchema, "404": ErrorSchema})
    def get_rates():  # noqa
        """Get user's BMR and TDEE rates."""
        session = Session()
        try:
            rates, error = get_user_rates(session)
            if error:
                return {"message": error}, 404
            return rates.model_dump()
        finally:
            session.close()

    @app.get('/stats/history', tags=[stats_tag], responses={"200": HistorySchema})
    def get_history():  # noqa
        """Get user's caloric history for the last 7 days."""
        session = Session()
        try:
            history = get_user_history(session)
            return history.model_dump()
        finally:
            session.close()
