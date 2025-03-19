from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from model.base import Base


class PersonalInfo(Base):
    """PersonalInfo model."""
    __tablename__ = 'personal_info'

    id = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    goal_id = Column(Integer, ForeignKey('goal.id'), nullable=False)
    activity_level_id = Column(Integer, ForeignKey(
        'activity_level.id'), nullable=False)
    date = Column(DateTime, nullable=False)

    # Relationships
    activity_level = relationship("ActivityLevel", backref="personal_infos")
    goal = relationship("Goal", backref="personal_infos")

    def __repr__(self):
        """String representation of the PersonalInfo model."""
        return f"<PersonalInfo(id={self.id}, age={self.age}, gender={self.gender}, height={self.height}, weight={self.weight}, goal_id={self.goal_id}, activity_level_id={self.activity_level_id}, date={self.date})>"
