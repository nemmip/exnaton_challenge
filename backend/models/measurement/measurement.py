from datetime import datetime

from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Integer, Uuid
from sqlalchemy.orm import relationship, validates

from ..base.base import Base


class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    muid = Column(Uuid, nullable=False)
    quality = Column(String, nullable=False)
    measurement = relationship('Measurement', back_populates='tags')

class Measurement(Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    measurement = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    energy = Column(Float, nullable=False)
    tags_id = Column(Integer, ForeignKey(Tags.id), nullable=False)

    # relationships
    tags = relationship(Tags, back_populates="measurement", uselist=False, cascade="all, delete-orphan",
                        single_parent=True)

    # validators
    @validates('value')
    def validate_value(self, key, value):
        if value < 0:
            raise ValueError(f'{key} must be greater than 0.')
