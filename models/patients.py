#!/usr/bin/python3
from models.parent_model import ParentModel
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from parent_model import ParentModel, Base


class Patient(ParentModel, Base):
    """
    Represents a patient in the hospital.
    """
    if models.storage_ENV == 'db':
    __tablename__ = 'patients'

    patient_id = Column(String(60), ForeignKey('patient.id'), autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    address = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    clinical_notes_summary = Column(Text, nullable=True)
    gender = Column(String(10), nullable=False)

    # Relationships
    Billing_and_Invoice = relationship("billing_and_payment", backref="patient")
    telehealths = relationship("TeleHealth", backref="patient")

    if models.storage_ENV != 'db':
        
        @classmethod
        def get_patient_bill(model):
            """Retrieves the bill of a patient"""
            total_amount = 0
            items = []
            for billing in self.billings:
                total_amount += billing.amount
                items.append(billing.to_dict())
            return {"total_amount": total_amount, "items": items}
        
        @classmethod
        def get_schedule(model, patient_id):
            """Returns the telehealth schedule of a patient"""
            now = datetime.utcnow()
            schedule = []
            for i in range(7):
                start_date = now + timedelta(days=i)
                end_date = start_date + timedelta(days=1)
                telehealths = model.query.filter(model.patient_id == patient_id, model.start_time >= 
                                             start_date, model.start_time < end_date).all()
            if telehealths:
                schedule.append({"date": start_date.strftime("%Y-%m-%d"), 
                                 "telehealths": [{"start_time": t.start_time, "provider_name": t.provider.name} 
                                     for t in telehealths]

        @classmethod
        def get_logs(model, patient_id, start_date, end_date):
        """Returns the telehealth logs of a patient in a given period"""
        logs = model.query.filter(model.patient_id == patient_id, model.start_time >= 
                                 start_date, model.start_time < end_date).all()
        return [{"start_time": l.start_time, "duration": l.duration, "provider_name": l.provider.name} 
                 for l in logs]       
