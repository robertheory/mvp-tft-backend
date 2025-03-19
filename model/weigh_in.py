from sqlalchemy import Column, Integer, Float, Date
from model.base import Base


class WeighIn(Base):
    """WeighIn model."""
    __tablename__ = 'weigh_in'

    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    def __repr__(self):
        """String representation of the WeighIn model."""
        return f"<WeighIn(id={self.id}, value={self.value}, date={self.date})>"
