import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from model.meal_food import MealFood
from .base import Base, uuid_gen


class Meal(Base):
    __tablename__ = 'meals'

    id = Column(String, primary_key=True, default=uuid_gen)
    title = Column(String(100), nullable=False)
    date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    meal_foods = relationship(
        'MealFood', back_populates='meal', cascade="all, delete-orphan")
    foods = relationship('Food', secondary='meal_foods', viewonly=True)

    def __init__(self, title, date):
        self.title = title
        self.date = date
        self.created_at = datetime.datetime.now()
        self.updated_at = None

    def add_food(self, food, quantity):
        self.foods.append(food)
        self.meal_foods.append(
            MealFood(meal=self, food=food, quantity=quantity))
        return self

    def remove_food(self, food):
        self.foods.remove(food)
        self.meal_foods = [
            meal_food for meal_food in self.meal_foods if meal_food.food != food]
        return self
