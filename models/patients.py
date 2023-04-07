#!/usr/bin/python3
from models.parent_model import ParentModel, Base
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
import models


class Patient(ParentModel, Base):
    """
    Represents a patient in the hospital.
    """
    if models.storage_ENV == 'db':
        __tablename__ = 'patients'

        patient_id = Column(String(60), ForeignKey('patients.id'), autoincrement=True, nullable=False)
        name = Column(String(255), nullable=False)
        age = Column(Integer, nullable=False)
        address = Column(String(255), nullable=True)
        phone_number = Column(String(20), nullable=True)
        email = Column(String(255), nullable=True)
        clinical_notes_summary = Column(Text, nullable=True)
        gender = Column(String(10), nullable=False)

        # Relationships
        Billings_and_Invoices = relationship("BillingInvoice", backref="Patient")
        Telehealths = relationship("TeleHealth", backref="Patient")

    if models.storage_ENV != 'db':
        
        @classmethod
        def get_patient_bill(cls):
            """Retrieves the bill of a patient"""
            total_amount = 0
            items = []
            for billing in cls.billings:
                total_amount += billing.amount
                items.append(billing.to_dict())
            return {"total_amount": total_amount, "items": items}
        
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
                if telehealths:
                    schedule.append({"date": start_date.strftime("%Y-%m-%d"), 
                                     "telehealths": [{"start_time": t.start_time, "provider_name": t.provider.name} 
                                         for t in telehealths]})
            return schedule

        @classmethod
        def get_logs(cls, patient_id, start_date, end_date):
            """Returns the telehealth logs of a patient in a given period"""
            logs = cls.query.filter(cls.patient_id == patient_id, cls.start_time >= 
                                      start_date, cls.start_time < end_date).all()
            return [{"start_time": l.start_time, "duration": l.duration, "provider_name": l.provider.name} 
                     for l in logs]
