#!/usr/bin/python3
from models.parent_model import ParentModel, Base
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
import models
from models.TeleHealth import TeleHealth


class Staff(ParentModel, Base):
    """Represents a staff member"""
    if models.storage_ENV == 'db':
        __tablename__ = "staff"

        name = Column(String(100), nullable=False)
        job_title = Column(String(100), nullable=False)
        department = Column(String(100), nullable=False)
        hire_date = Column(Date, nullable=True)
        email = Column(String(100), nullable=False)
        phone_number = Column(String(20), nullable=False)
        address = Column(String(200), nullable=False)
        role = Column(String(100), nullable=False)
        
        # Relationship
        TeleHealth = relationship("TeleHealth", back_populates="Staff")

    if models.storage_ENV != 'db':
        @classmethod
        def get_by_id(cls, id):
            """
            Retrieve a staff member by ID
            """
            return cls.query.filter_by(staff=id).first()

        @classmethod
        def count(cls):
            """
            Count the number of staff members
            """
            return cls.query.count()

        @classmethod
        def get_telehealth_activities(cls, id):
            """
            Retrieve the telehealth activities of this staff member
            """
            return TeleHealth.query.filter_by(staff=id).all()
