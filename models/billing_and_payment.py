from typing import Dict, List
from datetime import datetime
from parent_model import ParentModel


class BillingInvoice(ParentModel):
    """Class for Billing and Invoice"""

    def __init__(self, patient_id: str, staff_id: str, insurance_id: str,
                 procedure_code: str, amount: float, paid: bool = False,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patient_id = patient_id
        self.staff_id = staff_id
        self.insurance_id = insurance_id
        self.procedure_code = procedure_code
        self.amount = amount
        self.paid = paid

    def to_dict(self) -> Dict:
        """Returns dictionary representation of object"""
        attr = super().to_dict()
        attr.update({
            "patient_id": self.patient_id,
            "staff_id": self.staff_id,
            "insurance_id": self.insurance_id,
            "procedure_code": self.procedure_code,
            "amount": self.amount,
            "paid": self.paid
        })
        return attr

    def __str__(self) -> str:
        """Returns string representation of object"""
        return f"[[{self.__class__.__name__}] ({self.id}) {self.patient_id}, {self.amount}]"

    @classmethod
    def create(cls, patient_id: str, staff_id: str, insurance_id: str,
               procedure_code: str, amount: float, paid: bool = False) -> 'BillingInvoice':
        """Creates new billing and invoice"""
        billing_invoice = cls(patient_id, staff_id, insurance_id, procedure_code, amount, paid=paid)
        billing_invoice.save()
        return billing_invoice

    @classmethod
    def get_all(cls) -> List['BillingInvoice']:
        """Returns all billing and invoices"""
        return [obj for obj in cls.all() if isinstance(obj, cls)]

    @classmethod
    def get_by_patient_id(cls, patient_id: str) -> List['BillingInvoice']:
        """Returns all billing and invoices for a given patient"""
        return [obj for obj in cls.all() if isinstance(obj, cls) and obj.patient_id == patient_id]

    @classmethod
    def get_by_staff_id(cls, staff_id: str) -> List['BillingInvoice']:
        """Returns all billing and invoices for a given staff member"""
        return [obj for obj in cls.all() if isinstance(obj, cls) and obj.staff_id == staff_id]

    @classmethod
    def get_by_insurance_id(cls, insurance_id: str) -> List['BillingInvoice']:
        """Returns all billing and invoices for a given insurance"""
        return [obj for obj in cls.all() if isinstance(obj, cls) and obj.insurance_id == insurance_id]

    @classmethod
    def get_by_date_range(cls, start_date: datetime, end_date: datetime) -> List['BillingInvoice']:
        """Returns all billing and invoices for a given date range"""
        return [obj for obj in cls.all() if isinstance(obj, cls) and start_date <= obj.created_at <= end_date]

    def mark_paid(self) -> None:
        """Marks the billing and invoice as paid"""
        self.paid = True
        self.updated_at = datetime.utcnow()
        self.save()

    def mark_unpaid(self) -> None:
        """Marks the billing and invoice as unpaid"""
        self.paid = False
        self.updated_at = datetime.utcnow()
        self.save()
