from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database.base import Base


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    category_name = Column(String)
    created_at = Column(String)
