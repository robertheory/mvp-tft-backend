from sqlalchemy import Column, Integer, String, Float
from model.base import Base


class ActivityLevel(Base):
    """ActivityLevel model."""
    __tablename__ = 'activity_level'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    multiplier = Column(Float, nullable=False)

    def __repr__(self):
        """String representation of the ActivityLevel model."""
        return f"<ActivityLevel(id={self.id}, name={self.name}, description={self.description}, multiplier={self.multiplier})>"
