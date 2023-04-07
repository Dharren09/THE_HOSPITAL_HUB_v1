#!/usr/bin/python3
import models
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from models.parent_model import ParentModel, Base
from models.patients import Patient


class Pharmacy(ParentModel, Base):
    """ Represents the pharmacy """
    if models.storage_ENV == 'db':
        __tablename__ = 'Pharmacy'

        name = Column(String(100), nullable=False)
        batch_number = Column(Integer, nullable=False)
        expiry_date = Column(Integer, nullable=False)
        quantity = Column(Integer, nullable=False)
        price = Column(Integer, nullable=False)

        # Relationships
        Telehealths = relationship("TeleHealth", back_populates="Pharmacy", cascade="all, delete")
        Billings_and_Invoices = relationship("BillingInvoice", back_populates="Pharmacy", cascade="all, delete")

    @classmethod
    def get_drugs_in_stock(cls):
        """Retrieves all the drugs in stock"""
        return cls.query.filter(cls.quantity > 0).all()

    @classmethod
    def get_expired_drugs(cls):
        """Retrieves all expired drugs"""
        return cls.query.filter(cls.expiry_date < datetime.now()).all()

    def get_drug_info(self):
        """Retrieves all information of an individual drug"""
        return {"name": self.name, "batch_number": self.batch_number, "expiry_date": self.expiry_date,
                "quantity": self.quantity, "price": self.price}

