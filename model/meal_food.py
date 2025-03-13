from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import Base


class MealFood(Base):
    __tablename__ = 'meal_foods'
    meal_id = Column(String, ForeignKey('meals.id'), primary_key=True)
    food_id = Column(String, ForeignKey('foods.id'), primary_key=True)
    quantity = Column(Integer, nullable=False)

    meal = relationship("Meal", back_populates="meal_foods")
    food = relationship("Food", back_populates="meal_foods")
