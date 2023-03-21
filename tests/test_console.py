#!/usr/bin?python3
""" tests my console application """
import io
import sys
import unittest
from console import THE_HOSPITAL_HUBCommand


class TestTHE_HOSPITAL_HUBCommand(unittest.TestCase):

    def setUp(self):
        """Create a THE_HOSPITAL_HUB command interpreter before each test"""
        self.console = THE_HOSPITAL_HUBCommand()

    def tearDown(self):
        """Clean up the THE_HOSPITAL_HUB command interpreter after each test"""
        del self.console

    def test_show(self):
        """Test the show command"""
        # Redirect stdout to a buffer to capture output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        # Call the show command with a valid class name and id
        self.console.onecmd("show Patient 123")
        # Reset stdout
        sys.stdout = sys.__stdout__
        # Check the output
        expected_output = "string representation of Patient instance with id 123\n"
        self.assertEqual(captured_output.getvalue(), expected_output)

        # Call the show command with a missing class name
        self.console.onecmd("show")
        expected_output = "** class name missing **\n"
        self.assertEqual(captured_output.getvalue(), expected_output)

        # Call the show command with a non-existent class name
        self.console.onecmd("show Foo 123")
        expected_output = "** class doesn't exist **\n"
        self.assertEqual(captured_output.getvalue(), expected_output)

        # Call the show command with a missing id
        self.console.onecmd("show Patient")
        expected_output = "** instance id missing **\n"
        self.assertEqual(captured_output.getvalue(), expected_output)

        # Call the show command with a non-existent id
        self.console.onecmd("show Patient 999")
        expected_output = "** no instance found **\n"
        self.assertEqual(captured_output.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()

