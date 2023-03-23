import unittest
from models.parent_model import ParentModel
from models.patients import Patient
from models.billing_and_payment import BillingInvoice


class TestBillingInvoice(unittest.TestCase):
    
    def setUp(self):
        self.patient = Patient('John Doe', 'johndoe@example.com', '123 Main St', '555-1234')
        self.invoice = BillingInvoice(self.patient, 'PROC1', 100.0)
        
    def test_constructor(self):
        self.assertEqual(self.invoice.patient, self.patient)
        self.assertEqual(self.invoice.procedure_code, 'PROC1')
        self.assertEqual(self.invoice.amount_billed, 100.0)
        self.assertEqual(self.invoice.amount_paid, 0.0)
        self.assertIsNone(self.invoice.reason_for_payment)
        
    def test_set_amount_paid(self):
        self.invoice.set_amount_paid(50.0)
        self.assertEqual(self.invoice.amount_paid, 50.0)
        
    def test_set_reason_for_payment(self):
        self.invoice.set_reason_for_payment('Payment for procedure')
        self.assertEqual(self.invoice.reason_for_payment, 'Payment for procedure')
        
    def test_str(self):
        expected_output = f"BillingInvoice(patient={self.patient.name}, procedure_code=PROC1, amount_billed=100.0, amount_paid=0.0, reason_for_payment=None)"
        self.assertEqual(str(self.invoice), expected_output)
        
    def test_repr(self):
        expected_output = f"BillingInvoice(patient={self.patient!r}, procedure_code='PROC1', amount_billed=100.0, amount_paid=0.0, reason_for_payment=None)"
        self.assertEqual(repr(self.invoice), expected_output)
        
if __name__ == '__main__':
    unittest.main()
