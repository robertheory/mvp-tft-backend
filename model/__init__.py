import json
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from sqlalchemy.ext.declarative import declarative_base

from model.base import Base
from model.food import Food
from model.meal import Meal
from model.caloric_goal import CaloricGoal
from model.meal_food import MealFood
from model.weigh_in import WeighIn
from model.activity_level import ActivityLevel

db_path = "database/"
if not os.path.exists(db_path):
    os.makedirs(db_path)

db_url = 'sqlite:///%s/db.sqlite3' % db_path

engine = create_engine(db_url, echo=False)

Session = sessionmaker(bind=engine)

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)

session = Session()

if not session.query(Food).all():
    """
    Load data from json file if no data is present in the database
    """

    print("No data found in the database: loading demo data from json file")

    with open('data/foods.json') as f:
        print("Loading json data")
        data = json.load(f)

        print(f'{len(data)} foods loaded')

        for food_data in data:
            food = Food(**food_data)
            session.add(food)
            session.commit()

        print("Data loaded")

        session.close()
