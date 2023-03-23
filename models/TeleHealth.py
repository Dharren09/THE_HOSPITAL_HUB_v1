#!/usr/bin/python3
from models.patients import Patient
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.parent_model import Base, ParentModel
import models


class TeleHealth(ParentModel, Base):
    """Class represents a telehealth session"""
    if models.storage_ENV == 'db':
        __tablename__ = "telehealths"

        patient_id = Column(String(60), ForeignKey('patient.id'), autoincrement=True, nullable=False)
        duration = Column(Integer, nullable=False)
        notes = Column(String(500))
        start_time = Column(String(20), nullable=False)
        end_time = Column(String(20), nullable=False)
        duration = Column(Integer, nullable=False)

        # Relationships
        patient = relationship("Patient", back_populates="telehealths")

    if models.storage_ENV != 'db':
        @classmethod
        def get_logs(cls, patient_id, start_date, end_date):
            """Returns the telehealth logs of a patient in a given period"""
            logs = cls.query.filter(cls.patient_id == patient_id, cls.start_time >= 
                                 start_date, cls.start_time < end_date).all()
            return [{"start_time": l.start_time, "duration": l.duration, "provider_name": l.provider.name} 
                    for l in logs]

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
