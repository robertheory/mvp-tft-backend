from sqlalchemy import Column, Integer, Float, Date
from model.base import Base


class CaloricGoal(Base):
    """Model for storing caloric goals."""
    __tablename__ = 'caloric_goals'

    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    def __repr__(self):
        return f"<CaloricGoal(value={self.value}, date={self.date})>"
