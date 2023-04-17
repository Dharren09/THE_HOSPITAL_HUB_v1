#!/usr/bin/python3
from models.parent_model import ParentModel, Base
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
import models

if models.storage_ENV == 'db':
    patient_pharmacy = Table("patients_pharmacy", Base.metadata,
                         Column("patient_id", String(60), ForeignKey("patients.patient_id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
                         Column("pharmacy_id", String(60), ForeignKey("pharmacy.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True))

class Patient(ParentModel, Base):
    """
    Represents a patient in the hospital.
    """
    if models.storage_ENV == 'db':
        __tablename__ = 'patients'

        patient_id = Column(String(60), primary_key=True, autoincrement=True, nullable=False)
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
            patient = cls.query.get(patient_id)
            billings = patient.Billings_and_Invoices
            total_amount = sum(billing.amount for billing in billings)
            items = [billing.to_dict() for billing in billings]
            return {"total_amount": total_amount, "items": items}

        @classmethod
        def get_schedule(cls, patient_id, date):
            """Returns the telehealth schedule of a patient for a specific date"""
            start_date = datetime.strptime(date, '%Y-%m-%d')
            end_date = start_date + timedelta(days=1)
            telehealths = cls.query.filter(cls.patient_id == patient_id, cls.start_time >= start_date, cls.start_time < end_date).all()
            schedule = {"date": start_date.strftime("%Y-%m-%d"), "telehealths": []}
            for t in telehealths:
                schedule["telehealths"].append({"start_time": t.start_time})
            return schedule
            
        @classmethod
        def get_logs(log_file, start_date=None, end_date=None):
            """Get logs from a log file within a specified date range"""
            logs = []
            try:
                with open(log_file, 'r') as f:
                    for line in f:
                        log = line.strip()
                        log_date = datetime.datetime.strptime(log.split(',')[0], '%Y-%m-%d %H:%M:%S')
                        if start_date and log_date < start_date:
                            continue
                        if end_date and log_date > end_date:
                            continue
                        logs.append(log)
            except FileNotFoundError:
                print(f"Error: Log file '{log_file}' not found")
            return logs
