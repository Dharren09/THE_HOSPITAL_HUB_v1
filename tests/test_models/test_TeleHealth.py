#!/usr/bin/python3

import unittest
from datetime import datetime
from models.TeleHealth import TeleHealth


class TestTeleHealth(unittest.TestCase):
    def setUp(self):
        self.session = TeleHealth(
            patient_id="12345",
            staff_id="67890",
            session_date="2023-03-11",
            session_time="16:00:00",
            session_length=40
        )

    def test_attributes(self):
        self.assertTrue(hasattr(self.session, "id"))
        self.assertIsInstance(self.session.id, str)
        self.assertTrue(hasattr(self.session, "created_at"))
        self.assertIsInstance(self.session.created_at, datetime)
        self.assertTrue(hasattr(self.session, "updated_at"))
        self.assertIsInstance(self.session.updated_at, datetime)
        self.assertEqual(self.session.patient_id, "12345")
        self.assertEqual(self.session.staff_id, "67890")
        self.assertEqual(self.session.session_date, "2023-03-11")
        self.assertEqual(self.session.session_time, "16:00:00")
        self.assertEqual(self.session.session_length, 40)

    def test_to_dict(self):
        expected_dict = {
            "id": self.session.id,
            "created_at": self.session.created_at.isoformat(),
            "updated_at": self.session.updated_at.isoformat(),
            "__class__": "TeleHealth",
            "patient_id": "12345",
            "staff_id": "67890",
            "session_date": "2023-03-11",
            "session_time": "16:00:00",
            "session_length": 40
        }
        self.assertDictEqual(self.session.to_dict(), expected_dict)

    def test_str(self):
        expected_str = "[[TeleHealth] ({}) {}]".format(self.session.id, self.session.to_dict())
        self.assertEqual(str(self.session), expected_str)


if __name__ == '__main__':
    unittest.main()
