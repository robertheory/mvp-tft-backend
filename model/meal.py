import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from .base import Base, uuid_gen
from .meal_food import meal_foods


class Meal(Base):
    __tablename__ = 'meals'

    id = Column(String, primary_key=True, default=uuid_gen)
    title = Column(String(100), nullable=False)
    date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    foods = relationship('Food', secondary=meal_foods, back_populates='meals')

    def __init__(self, title, date):
        self.title = title
        self.date = date
        self.created_at = datetime.datetime.now()
        self.updated_at = None

    def add_food(self, food):
        self.foods.append(food)
        return self

    def remove_food(self, food):
        self.foods.remove(food)
        return self
