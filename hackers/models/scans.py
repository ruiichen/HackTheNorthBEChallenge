from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import backref, relationship
from ..database.base import Base
from ..models.hackers import Hackers
from ..models.activities import Activities


class Scans(Base):
    __tablename__ = 'scans'

    scan_id = Column(Integer, primary_key=True, autoincrement=True)
    hacker_uuid= Column(String, ForeignKey("hackers.uuid"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.activity_id"), nullable=False, index=True)
    scanned_at = Column(String)

    # Relationships
    hacker = relationship(
        Hackers,
        backref=backref('scans', uselist=True, cascade='delete,all')
    )
    activity = relationship(
        Activities,
        backref=backref('scans', uselist=True, cascade='delete,all')
    )
