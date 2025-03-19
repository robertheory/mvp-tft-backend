from sqlalchemy import Column, Integer, Float, Date
from model.base import Base


class CaloricGoal(Base):
    """Model for storing caloric goals."""
    __tablename__ = 'caloric_goals'

    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    def __repr__(self):
        return f"<CaloricGoal(value={self.value}, start_date={self.start_date}, end_date={self.end_date})>"
