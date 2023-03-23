import unittest
from io import StringIO
import sys
from console import THE_HOSPITAL_HUBCommand


class TestConsole(unittest.TestCase):
    def setUp(self):
        """Set up the console before each test"""
        self.console = THE_HOSPITAL_HUBCommand()
        self.held, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        """Clean up the console after each test"""
        sys.stdout = self.held

    def test_create(self):
        """Test the create command"""
        self.console.onecmd("create Patient name='John Doe' age=25 gender='Male'")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Patient.create(1)")

    def test_show(self):
        """Test the show command"""
        self.console.onecmd("create Patient name='John Doe' age=25 gender='Male'")
        self.console.onecmd("show Patient 1")
        output = sys.stdout.getvalue().strip()
        self.assertTrue("John Doe" in output)
        self.assertTrue("25" in output)
        self.assertTrue("Male" in output)

    def test_do_update(self):
        """Test the do_update command"""
        self.console.onecmd("create Patient name='John Doe' age=25 gender='Male'")
        self.console.onecmd("update Patient 1 name 'Jane Doe'")
        self.console.onecmd("show Patient 1")
        output = sys.stdout.getvalue().strip()
        self.assertTrue("Jane Doe" in output)

    def test_do_all(self):
        """Test the do_all command"""
        self.console.onecmd("create Patient name='John Doe' age=25 gender='Male'")
        self.console.onecmd("create Patient name='Jane Doe' age=30 gender='Female'")
        self.console.onecmd("create Doctor name='Dr. Smith' specialty='Cardiology'")
        self.console.onecmd("all")
        output = sys.stdout.getvalue().strip()
        self.assertTrue("John Doe" in output)
        self.assertTrue("Jane Doe" in output)
        self.assertTrue("Dr. Smith" in output)
        self.assertTrue("Cardiology" in output)
        self.assertTrue("Patient" in output)
        self.assertTrue("Doctor" in output)


if __name__ == '__main__':
    unittest.main()
