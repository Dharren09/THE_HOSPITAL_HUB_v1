#!/usr/bin/python3
import models
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from models.parent_model import ParentModel, Base


class Pharmacy(ParentModel, Base):
    """ Represents the pharmacy """
    if models.storage_ENV == 'db':
        __tablename__ = 'Pharmacy'

        patient_id = Column(String(60), ForeignKey('patient.id'), autoincrement=True, nullable=False)
        name = Column(String(100), nullable=False)
        batch_number = Column(integer, nullable=False)
        expiry_date = Column(integer, nullable=False)
        quantity = Column(integer, nullable=False)
        price = Column(integer, nullable=False)

        # Relationships
        telehealths = relationship("TeleHealth", back_populates="pharmacy")
        billing_invoice = relationship("BillingInvoice", back_populates="pharmacy")

    @classmethod
    def get_drugs_in_stock(model):
        """Retrieves all the drugs in stock"""
        return cls.query.filter(cls.quantity > 0).all()

    @classmethod
    def get_expired_drugs(model):
        """Retrieves all expired drugs"""
        return cls.query.filter(cls.expiry_date < datetime.now()).all()

    def get_drug_info(self):
        """Retrieves all information of an individual drug"""
        return {"name": self.name, "batch_number": self.batch_number, "expiry_date": self.expiry_date,
                "quantity": self.quantity, "price": self.price}
