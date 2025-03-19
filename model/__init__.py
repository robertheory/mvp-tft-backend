import json
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from sqlalchemy.ext.declarative import declarative_base

from model.base import Base
from model.food import Food
from model.meal import Meal
from model.meal_food import MealFood
from model.activity_level import ActivityLevel
from model.personal_info import PersonalInfo
from model.goal import Goal

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

# Load demo data if no data is present
if not session.query(Food).all():
    print("No data found in the database: loading demo data from json file")

    # Load foods
    with open('data/foods.json') as f:
        print("Loading foods data")
        data = json.load(f)
        print(f'{len(data)} foods loaded')
        for food_data in data:
            food = Food(**food_data)
            session.add(food)
        session.commit()
        print("Foods data loaded")

    # Load activity levels
    with open('data/activity_levels.json') as f:
        print("Loading activity levels data")
        data = json.load(f)
        print(f'{len(data)} activity levels loaded')
        for level_id, level_data in data.items():
            activity_level = ActivityLevel(
                id=int(level_id),
                name=level_data['name'],
                description=level_data['description'],
                multiplier=level_data['multiplier']
            )
            session.add(activity_level)
        session.commit()
        print("Activity levels data loaded")

    # Load goals
    with open('data/goals.json') as f:
        print("Loading goals data")
        data = json.load(f)
        print(f'{len(data)} goals loaded')
        for goal_id, goal_data in data.items():
            goal = Goal(
                id=int(goal_id),
                name=goal_data['name'],
                rate=goal_data['rate']
            )
            session.add(goal)
        session.commit()
        print("Goals data loaded")

    session.close()
