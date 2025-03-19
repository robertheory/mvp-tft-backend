from sqlalchemy import Column, Integer, String, Date
from model.base import Base


class ActivityLevel(Base):
    """ActivityLevel model."""
    __tablename__ = 'activity_level'

    id = Column(Integer, primary_key=True)
    level = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    def __repr__(self):
        """String representation of the ActivityLevel model."""
        return f"<ActivityLevel(id={self.id}, level={self.level}, date={self.date})>"
