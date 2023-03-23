import unittest
from datetime import datetime
from models.pharmacy import Pharmacy


class TestPharmacy(unittest.TestCase):
    def setUp(self):
        self.pharmacy = Pharmacy(name="Drug A", batch_number=123, expiry_date=datetime.now(),
                                 quantity=10, price=5.99)
    
    def test_get_drugs_in_stock(self):
        self.assertEqual(Pharmacy.get_drugs_in_stock(), [self.pharmacy])
        
        # Add a drug with zero quantity
        Pharmacy(name="Drug B", batch_number=456, expiry_date=datetime.now(),
                 quantity=0, price=3.99)
        self.assertEqual(Pharmacy.get_drugs_in_stock(), [self.pharmacy])
    
    def test_get_expired_drugs(self):
        self.assertEqual(Pharmacy.get_expired_drugs(), [])
        
        # Add a drug with expired expiry_date
        Pharmacy(name="Drug C", batch_number=789, expiry_date=datetime(2022, 1, 1),
                 quantity=5, price=9.99)
        self.assertEqual(Pharmacy.get_expired_drugs(), [self.pharmacy])
        
    def test_get_drug_info(self):
        expected_info = {"name": "Drug A", "batch_number": 123, "expiry_date": datetime.now(),
                         "quantity": 10, "price": 5.99}
        self.assertEqual(self.pharmacy.get_drug_info(), expected_info)


if __name__ == '__main__':
    unittest.main()
