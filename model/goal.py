from sqlalchemy import Column, Integer, String, Float
from model.base import Base


class Goal(Base):
    """Goal model."""
    __tablename__ = 'goal'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    rate = Column(Float, nullable=False)

    def __repr__(self):
        """String representation of the Goal model."""
        return f"<Goal(id={self.id}, name={self.name}, rate={self.rate})>"
