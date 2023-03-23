#!/usr/bin/python3
from datetime import datetime
from models.patients import Patient
from models.parent_model import ParentModel, Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Float
import models



class BillingInvoice(ParentModel, Base):
    """Class for Billing and Invoice for individual patients"""
    if models.storage_ENV == 'db':
        __tablename__ = "Billings_and_Invoices"
        
        patient_id = Column(String(60), ForeignKey('patient.id'), autoincrement=True, nullable=False)
        procedure_code = Column(String(36), nullable=False)
        amount_billed = Column(Float, nullable=False)
        amount_paid = Column(Float, nullable=False)
        reason_for_payment = Column(String(255), nullable=True)
