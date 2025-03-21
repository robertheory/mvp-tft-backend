import datetime
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from .base import Base, uuid_gen


class Food(Base):
    __tablename__ = 'foods'

    id = Column(String, primary_key=True, default=uuid_gen)
    name = Column(String(100), nullable=False)
    unit = Column(String(10), nullable=False)
    calories = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    meal_foods = relationship('MealFood', back_populates='food')

    def __init__(self, name, unit, calories):
        self.id = uuid_gen()
        self.name = name
        self.unit = unit
        self.calories = calories
        self.created_at = datetime.datetime.now()
        self.updated_at = None
