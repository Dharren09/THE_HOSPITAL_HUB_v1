import unittest
import os
import json
from datetime import datetime
from models.patients import Patient
from models.staff import Staff
from models.pharmacy import Pharmacy
from models.billing_and_payment import BillingInvoice
from models.TeleHealth import TeleHealth
from models.file_storage import FileStorage

class TestFileStorage(unittest.TestCase):

    def setUp(self):
        self.fs = FileStorage()

    def tearDown(self):
        os.remove("file.json")

    def test_all(self):
        # create some objects and add them to the file storage
        patient1 = Patient(name="John Doe")
        self.fs.new(patient1)
        staff1 = Staff(name="Jane Smith")
        self.fs.new(staff1)
        billing1 = BillingInvoice(patient_id=patient1.id, staff_id=staff1.id, amount=100.0)
        self.fs.new(billing1)

        # test getting all objects
        all_objs = self.fs.all()
        self.assertIn("Patient.{}".format(patient1.id), all_objs)
        self.assertIn("Staff.{}".format(staff1.id), all_objs)
        self.assertIn("BillingInvoice.{}".format(billing1.id), all_objs)

        # test getting objects of a certain class
        patient_objs = self.fs.all(model=Patient)
        self.assertIn("Patient.{}".format(patient1.id), patient_objs)
        self.assertNotIn("Staff.{}".format(staff1.id), patient_objs)
        self.assertNotIn("BillingInvoice.{}".format(billing1.id), patient_objs)

    def test_new(self):
        # create a patient object
        patient1 = Patient(name="John Doe")

        # add the object to the file storage
        self.fs.new(patient1)

        # make sure the object was added
        all_objs = self.fs.all()
        self.assertIn("Patient.{}".format(patient1.id), all_objs)

    def test_save_reload(self):
        # create some objects and add them to the file storage
        patient1 = Patient(name="John Doe")
        self.fs.new(patient1)
        staff1 = Staff(name="Jane Smith")
        self.fs.new(staff1)
        billing1 = BillingInvoice(patient_id=patient1.id, staff_id=staff1.id, amount=100.0)
        self.fs.new(billing1)

        # save the file storage to disk
        self.fs.save()

        # reload the file storage from disk
        self.fs.reload()

        # test that the objects were reloaded correctly
        all_objs = self.fs.all()
        self.assertIn("Patient.{}".format(patient1.id), all_objs)
        self.assertIn("Staff.{}".format(staff1.id), all_objs)
        self.assertIn("BillingInvoice.{}".format(billing1.id), all_objs)

    def test_create(self):
        # test create() with Patient
        patient_obj = self.storage.create('Patient', first_name='Alice', last_name='Smith')
        all_objs = self.storage.all(model=Patient)
        self.assertIsInstance(patient_obj, Patient)
        self.assertIn(patient_obj.id, all_objs)
        self.assertEqual(patient_obj.first_name, 'Alice')
        self.assertEqual(patient_obj.last_name, 'Smith')

        # test create() with Staff
        staff_obj = self.storage.create('Staff', first_name='Bob', last_name='Johnson', position='doctor')
        all_objs = self.storage.all(model=Staff)
        self.assertIsInstance(staff_obj, Staff)
        self.assertIn(staff_obj.id, all_objs)
        self.assertEqual(staff_obj.first_name, 'Bob')
        self.assertEqual(staff_obj.last_name, 'Johnson')
        self.assertEqual(staff_obj.position, 'doctor')

        # test create() with Pharmacy
        pharmacy_obj = self.storage.create('Pharmacy', name='pharmacy', location='san francisco')
        all_objs = self.storage.all(model=Pharmacy)
        self.assertIsInstance(pharmacy_obj, Pharmacy)
        self.assertIn(pharmacy_obj.id, all_objs)
        self.assertEqual(pharmacy_obj.name, 'pharmacy')
        self.assertEqual(pharmacy_obj.location, 'san francisco')

        # test create() with BillingInvoice
        invoice_obj = self.storage.create('BillingInvoice', patient_id=self.patient.id, total_amount=100)
        all_objs = self.storage.all(model=BillingInvoice)
        self.assertIsInstance(invoice_obj, BillingInvoice)
        self.assertIn(invoice_obj.id, all_objs)
        self.assertEqual(invoice_obj.patient_id, self.patient.id)
        self.assertEqual(invoice_obj.total_amount, 100)

        # test create() with TeleHealth
        telehealth_obj = self.storage.create('TeleHealth', staff_id=self.staff.id, patient_id=self.patient.id)
        all_objs = self.storage.all(model=TeleHealth)
        self.assertIsInstance(telehealth_obj, TeleHealth)
        self.assertIn(telehealth_obj.id, all_objs)
        self.assertEqual(telehealth_obj.staff_id, self.staff.id)
        self.assertEqual(telehealth_obj.patient_id, self.patient.id)

    def test_get(self):
        # test get() with valid model and id
        self.storage.new(self.patient)
        self.storage.new(self.staff)
        self.storage.new(self.pharmacy)
        self.storage.new(self.invoice)
        self.storage.new(self.telehealth)
        self.storage.save()
        obj = self.storage.get("Patient", self.patient.id)
        self.assertIsInstance(obj, Patient)
        self.assertEqual(obj.first_name, self.patient.first_name)
        self.assertEqual(obj.last_name, self.patient.last_name)
        obj = self.storage.get("Staff", self.staff.id)
        self.assertIsInstance(obj, Staff)
        self.assertEqual(obj.first_name, self.staff.first_name)
        self.assertEqual(obj.last_name, self.staff.last_name)
        self.assertEqual(obj.position, self.staff.position)

        # test get() with invalid model and id
        obj = self.storage.get("InvalidModel", "invalid_id")
        self.assertIsNone(obj)
        obj = self.storage.get("Patient", "invalid_id")
        self.assertIsNone(obj)

    def test_delete(self):
        # test deleting an object
        obj_key = "{}.{}".format(Patient.__name__, self.patient.id)
        self.assertIn(obj_key, FileStorage._FileStorage__objects)
        self.storage.delete(self.patient.id)
        self.assertNotIn(obj_key, FileStorage._FileStorage__objects)

        # test deleting a non-existent object
        with self.assertRaises(KeyError):
            self.storage.delete("non-existent-id")

        # test saving after deletion
        obj_key = "{}.{}".format(Staff.__name__, self.staff.id)
        self.assertIn(obj_key, FileStorage._FileStorage__objects)
        self.storage.delete(self.staff.id)
        self.assertNotIn(obj_key, FileStorage._FileStorage__objects)
        self.storage.save()
        with open(FileStorage._FileStorage__file_path, "r") as f:
            file_content = json.load(f)
            self.assertNotIn(obj_key, file_content)

    def test_count_objects_by_class(self):
        # test count() with objects of a certain class
        self.storage.new(self.patient)
        self.storage.new(self.staff)
        self.storage.new(self.pharmacy)
        self.storage.new(self.invoice)
        self.storage.new(self.telehealth)
        self.assertEqual(self.storage.count(model=Patient), 1)
        self.assertEqual(self.storage.count(model=Staff), 1)
        self.assertEqual(self.storage.count(model=Pharmacy), 1)
        self.assertEqual(self.storage.count(model=BillingInvoice), 1)
        self.assertEqual(self.storage.count(model=TeleHealth), 1)

    def test_count_objects_by_class_not_in_storage(self):
        # test count() with objects of a certain class that are not in storage
        self.assertEqual(self.storage.count(model=Patient), 0)
        self.assertEqual(self.storage.count(model=Staff), 0)
        self.assertEqual(self.storage.count(model=Pharmacy), 0)
        self.assertEqual(self.storage.count(model=BillingInvoice), 0)
        self.assertEqual(self.storage.count(model=TeleHealth), 0)

    def test_update(self):
        # Create a User object
        user = self.storage.create("User", email="test@example.com", password="testpassword")

       # Update the user object with new values
       updates = {"email": "newemail@example.com", "password": "newpassword"}
       self.storage.update(user, updates)

       # Get the user object by ID
       updated_user = self.storage.get("User", user.id)

       # Check that the updated values match
       self.assertEqual(updated_user.email, updates["email"])
       self.assertEqual(updated_user.password, updates["password"])

    def test_update_with_invalid_field(self):
       # Create a User object
       user = self.storage.create("User", email="test@example.com", password="testpassword")

       # Update the user object with an invalid field
       updates = {"invalid_field": "newvalue"}

       # Check that an AttributeError is raised
       with self.assertRaises(AttributeError):
           self.storage.update(user, updates)

    def test_update_with_readonly_field(self):
       # Create a User object
       user = self.storage.create("User", email="test@example.com", password="testpassword")

       # Update the user object with a readonly field
       updates = {"created_at": "2022-03-23T00:00:00"}

       # Check that an AttributeError is raised
       with self.assertRaises(AttributeError):
           self.storage.update(user, updates)


if __name__ == "__main__":
    unittest.main()
