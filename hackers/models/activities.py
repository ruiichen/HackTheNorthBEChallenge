from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from ..database.base import Base
from ..models.categories import Categories

class Activities(Base):
    __tablename__ = 'activities'

    activity_id =  Column(Integer, primary_key=True, index=True)
    activity_name = Column(String, unique=True)
    category_id = Column(Integer,  ForeignKey("categories.id"), nullable=False)
    created_at = Column(String)

    category = relationship(
        Categories,
        backref=backref('scans', uselist=True, cascade='delete,all')
    )
