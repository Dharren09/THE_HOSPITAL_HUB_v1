#!/usr/bin/python3
# tests all parameters in the parent_model.py to ensure it performs as prompted

import unittest
from datetime import datetime
from parent_model import ParentModel


class TestParentModel(unittest.TestCase):

    def setUp(self):
        self.model = ParentModel(name="Test", value=123)

    def test_id_is_string(self):
        self.assertIsInstance(self.model.id, str)

    def test_created_at_is_datetime(self):
        self.assertIsInstance(self.model.created_at, datetime)

    def test_updated_at_is_datetime(self):
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_created_at_is_before_updated_at(self):
        self.assertLess(self.model.created_at, self.model.updated_at)

    def test_to_dict_returns_dict(self):
        d = self.model.to_dict()
        self.assertIsInstance(d, dict)

    def test_to_dict_includes_class_name(self):
        d = self.model.to_dict()
        self.assertIn("__class__", d)
        self.assertEqual(d["__class__"], "ParentModel")

    def test_to_dict_includes_all_attributes(self):
        d = self.model.to_dict()
        self.assertIn("id", d)
        self.assertIn("name", d)
        self.assertIn("value", d)
        self.assertIn("created_at", d)
        self.assertIn("updated_at", d)

    def test_to_dict_includes_created_at_as_string(self):
        d = self.model.to_dict()
        self.assertIsInstance(d["created_at"], str)
        self.assertEqual(d["created_at"], self.model.created_at.isoformat())

    def test_to_dict_includes_updated_at_as_string(self):
        d = self.model.to_dict()
        self.assertIsInstance(d["updated_at"], str)
        self.assertEqual(d["updated_at"], self.model.updated_at.isoformat())

    def test_str_returns_string(self):
        s = str(self.model)
        self.assertIsInstance(s, str)

    def test_str_contains_class_name(self):
        s = str(self.model)
        self.assertIn("ParentModel", s)

    def test_str_contains_id(self):
        s = str(self.model)
        self.assertIn(self.model.id, s)

    def test_str_contains_attributes(self):
        s = str(self.model)
        self.assertIn("name", s)
        self.assertIn("Test", s)
        self.assertIn("value", s)
        self.assertIn("123", s)
        self.assertIn("created_at", s)
        self.assertIn("updated_at", s)

    def test_save_updates_updated_at(self):
        original_updated_at = self.model.updated_at
        self.model.save()
        self.assertGreater(self.model.updated_at, original_updated_at)


if __name__ == '__main__':
    unittest.main()
