from parent_model import ParentModel
import uuid
from datetime import datetime


class Staff(ParentModel):
    """Represents a staff member"""
    def __init__(self, first_name: str, last_name: str, email: str,
            password: str, job_specification: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.job_specification = job_specification

    def to_dict(self):
        """Returns dictionary representation of object"""
        attr = super().to_dict()
        attr["first_name"] = self.first_name
        attr["last_name"] = self.last_name
        attr["email"] = self.email
        attr["password"] = self.password
        attr["job_specification"] = self.job_specification
        return attr

    def __str__(self):
        """Returns string representation of object"""
        return f"[Staff] ({self.id}) {self.first_name} {self.last_name}"

