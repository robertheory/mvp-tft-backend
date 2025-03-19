from sqlalchemy import Column, Integer, String, Date
from model import Base


class ActivityLevel(Base):
    """Model for activity levels."""
    __tablename__ = 'activity_level'

    id = Column(Integer, primary_key=True)
    level = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    def __repr__(self):
        """String representation of the ActivityLevel model."""
        return f"<ActivityLevel(id={self.id}, level={self.level}, start_date={self.start_date}, end_date={self.end_date})>"
