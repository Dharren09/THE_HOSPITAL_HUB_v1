from parent_model import ParentModel
from datetime import date


class Patient(ParentModel):
    """
    Represents a patient in the hospital.
    """

    def __init__(self, first_name, last_name, date_of_birth, gender, address, phone_number, email):
        """
        Initializes a new instance of the Patient class.

        Args:
            first_name (str): The patient's first name.
            last_name (str): The patient's last name.
            date_of_birth (date): The patient's date of birth.
            gender (str): The patient's gender.
            address (str): The patient's address.
            phone_number (str): The patient's phone number.
            email (str): The patient's email address.
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.admission_date = None
        self.discharge_date = None
        self.treatment_summary = None

    def admit(self):
        """
        Admits the patient to the hospital.
        """
        self.admission_date = date.today()

    def discharge(self):
        """
        Discharges the patient from the hospital.
        """
        self.discharge_date = date.today()

    def update_treatment_summary(self, summary):
        """
        Updates the patient's treatment summary.

        Args:
            summary (str): The updated treatment summary.
        """
        self.treatment_summary = summary

    def __str__(self):
        """
        Returns a string representation of the Patient object.
        """
        return f"Patient: {self.first_name} {self.last_name}, DOB: {self.date_of_birth}, Gender: {self.gender}, " \
               f"Address: {self.address}, Phone: {self.phone_number}, Email: {self.email}, " \
               f"Admitted: {self.admission_date}, Discharged: {self.discharge_date}, " \
               f"Treatment Summary: {self.treatment_summary}"

