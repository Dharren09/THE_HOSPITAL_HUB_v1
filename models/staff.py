#!/usr/bin/python3
from models.parent_model import ParentModel
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship


class Staff(ParentModel, Base):
    """Represents a staff member"""
    if models.storage_env == 'db':
        __tablename__ = "staffs"

        name = Column(String(100), nullable=False)
        job_title = Column(String(100), nullable=False)
        department = Column(String(100), nullable=False)
        hire_date = Column(Date, nullable=False)
        email = Column(String(100), nullable=False)
        phone_number = Column(String(20), nullable=False)
        address = Column(String(200), nullable=False)
        role = Column(String(100), nullable=False)
        staff_id = Column(String(36), primary_key("staff.id"), nullable=False)
        
        # Relationship
        TeleHealth = relationship("TeleHealth", back_populates="staffs")

    if models.storage_env != 'db':
        @classmethod
        def get_by_id(cls, staff_id):
            """
            Retrieve a staff member by ID
            """
            return cls.query.filter_by(staff_id=staff_id).first()

        @classmethod
            def count(cls):
            """
            Count the number of staff members
            """
            return cls.query.count()

        @classmethod
        def get_telehealth_activities(self):
            """
            Retrieve the telehealth activities of this staff member
            """
            return TeleHealth.query.filter_by(staff_id=self.staff_id).all()
