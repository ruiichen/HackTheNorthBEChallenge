from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..database.base import Base


class Hackers(Base):
    __tablename__ = 'hackers'

    uuid = Column(String, primary_key=True, index=True)
    badge_code = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    updated_at = Column(String)
