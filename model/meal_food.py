from sqlalchemy import Table, Column, String, ForeignKey, Integer
from .base import Base

meal_foods = Table('meal_foods', Base.metadata,
                   Column('meal_id', String, ForeignKey(
                       'meals.id'), primary_key=True),
                   Column('food_id', String, ForeignKey(
                       'foods.id'), primary_key=True),
                   Column('quantity', Integer, nullable=False)
                   )
