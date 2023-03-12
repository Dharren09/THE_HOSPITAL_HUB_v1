from typing import List, Dict
from parent_model import ParentModel


class Career(ParentModel):
    """Class representing career opportunities"""
    def __init__(self, name: str, requirements: List[str], description: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.requirements = requirements
        self.description = description

    def to_dict(self) -> Dict:
        """Returns dictionary representation of object"""
        attr = super().to_dict()
        attr.update({
            "name": self.name,
            "requirements": self.requirements,
            "description": self.description,
        })
        return attr


class CareerAlert(ParentModel):
    """Class representing career alerts"""
    def __init__(self, career: Career, email: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.career = career
        self.email = email
        self.status = "Pending"  # can be Pending, Accepted, or Declined

    def to_dict(self) -> Dict:
        """Returns dictionary representation of object"""
        attr = super().to_dict()
        attr.update({
            "career": self.career.to_dict(),
            "email": self.email,
            "status": self.status,
        })
        return attr
"""Both classes have a to_dict() method that returns a dictionary representation of the object. The Career class simply adds its attributes to the dictionary returned by the parent to_dict() method, while the CareerAlert class calls the to_dict() method of its Career attribute and adds that dictionary to its own dictionary representation"""
