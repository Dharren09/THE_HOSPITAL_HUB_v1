import unittest
from datetime import datetime, timedelta
from models.patients import Patient
from models.Telehealth import TeleHealth


class TestTeleHealth(unittest.TestCase):

    def test_subclass(self):
        self.assertTrue(issubclass(TeleHealth, ParentModel))
        self.assertTrue(issubclass(TeleHealth, Base))

    def test_attributes(self):
        self.assertTrue(hasattr(TeleHealth, 'patient_id'))
        self.assertTrue(hasattr(TeleHealth, 'duration'))
        self.assertTrue(hasattr(TeleHealth, 'notes'))
        self.assertTrue(hasattr(TeleHealth, 'start_time'))
        self.assertTrue(hasattr(TeleHealth, 'end_time'))

    def test_relationship(self):
        self.assertTrue(hasattr(TeleHealth, 'patient'))
        self.assertEqual(TeleHealth.patient.property.mapper.class_, Patient)

    def test_get_logs(self):
        logs = TeleHealth.get_logs(patient_id='1', start_date='2022-01-01', end_date='2022-01-07')
        expected_logs = [
            {
                "start_time": "2022-01-02 14:30:00",
                "duration": 30,
                "provider_name": "Dr. Smith"
            },
            {
                "start_time": "2022-01-03 10:00:00",
                "duration": 60,
                "provider_name": "Dr. Johnson"
            }
        ]
        self.assertListEqual(logs, expected_logs)

    def test_get_schedule(self):
        schedule = TeleHealth.get_schedule(patient_id='1')
        expected_schedule = [
            {
                "date": (datetime.utcnow() + timedelta(days=i)).strftime("%Y-%m-%d"),
                "telehealths": [
                    {"start_time": "2022-01-02 14:30:00"}
                ]
            } for i in range(7)
        ]
        self.assertListEqual(schedule, expected_schedule)


if __name__ == '__main__':
    unittest.main()
