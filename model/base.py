from sqlalchemy.ext.declarative import declarative_base
import uuid


def uuid_gen():
    return str(uuid.uuid4())


Base = declarative_base()
