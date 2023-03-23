import unittest
from datetime import date
from unittest.mock import patch
from models.staff import Staff

class TestStaff(unittest.TestCase):
    def setUp(self):
        self.staff = Staff(
            name="John Doe",
            job_title="Nurse",
            department="Emergency",
            hire_date=date(2021, 1, 1),
            email="john.doe@example.com",
            phone_number="1234567890",
            address="123 Main St, Anytown USA",
            role="nurse",
            staff_id="12345"
        )

    def test_create_staff(self):
        self.assertEqual(self.staff.name, "John Doe")
        self.assertEqual(self.staff.job_title, "Nurse")
        self.assertEqual(self.staff.department, "Emergency")
        self.assertEqual(self.staff.hire_date, date(2021, 1, 1))
        self.assertEqual(self.staff.email, "john.doe@example.com")
        self.assertEqual(self.staff.phone_number, "1234567890")
        self.assertEqual(self.staff.address, "123 Main St, Anytown USA")
        self.assertEqual(self.staff.role, "nurse")
        self.assertEqual(self.staff.staff_id, "12345")

    def test_get_by_id(self):
        with patch.object(Staff, "query") as mock_query:
            mock_query.filter_by.return_value.first.return_value = self.staff

            result = Staff.get_by_id("12345")

            mock_query.filter_by.assert_called_once_with(staff_id="12345")
            mock_query.filter_by.return_value.first.assert_called_once_with()
            self.assertEqual(result, self.staff)

    def test_count(self):
        with patch.object(Staff, "query") as mock_query:
            mock_query.count.return_value = 2

            result = Staff.count()

            mock_query.count.assert_called_once_with()
            self.assertEqual(result, 2)

    def test_get_telehealth_activities(self):
        with patch.object(Staff, "query") as mock_query, \
             patch.object(Staff, "TeleHealth") as mock_telehealth:
            mock_query.filter_by.return_value.first.return_value = self.staff
            mock_telehealth.query.filter_by.return_value.all.return_value = []

            result = self.staff.get_telehealth_activities()

            mock_query.filter_by.assert_called_once_with(staff_id="12345")
            mock_query.filter_by.return_value.first.assert_called_once_with()
            mock_telehealth.query.filter_by.assert_called_once_with(staff_id="12345")
            mock_telehealth.query.filter_by.return_value.all.assert_called_once_with()
            self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()

