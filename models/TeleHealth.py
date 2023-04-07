#!/usr/bin/python3
from models.patients import Patient
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.parent_model import Base, ParentModel
import models
from datetime import datetime, timedelta


class TeleHealth(ParentModel, Base):
    """Class represents a telehealth session"""
    if models.storage_ENV == 'db':
        __tablename__ = "Telehealth"

        id = Column(Integer, primary_key=True, autoincrement=True)
        duration = Column(Integer, nullable=False)
        notes = Column(String(500), nullable=True)
        start_time = Column(String(20), nullable=False)
        end_time = Column(String(20), nullable=False)

        # Relationships
        patient_id = Column(String(60), ForeignKey('patients.patient_id'), nullable=False)
        patient = relationship("Patient", back_populates="Telehealth")

    if models.storage_ENV != 'db':
        @classmethod
        def get_logs(cls, patient_id, start_date, end_date):
            """Returns the telehealth logs of a patient in a given period"""
            logs = cls.query.filter(cls.patient_id == patient_id, cls.start_time >= 
                                 start_date, cls.start_time < end_date).all()
            return [{"start_time": l.start_time, "duration": l.duration} for l in logs]

        @classmethod
        def get_schedule(cls, patient_id):
            """Returns the telehealth schedule of a patient"""
            now = datetime.utcnow()
            schedule = []
            for i in range(7):
                start_date = now + timedelta(days=i)
                end_date = start_date + timedelta(days=1)
                telehealths = cls.query.filter(cls.patient_id == patient_id, cls.start_time >= 
                                            start_date, cls.start_time < end_date).all()
                schedule.append({"date": start_date.strftime("%Y-%m-%d"), "telehealths": 
                                [{"start_time": t.start_time} for t in telehealths]
                                 })
            return schedule
