from typing import Dict, List
from parent_model import ParentModel


class Insurance(ParentModel):
    """Class represents an insurance holder"""

    def __init__(self, name: str, address: str, phone: str, email: str,
                 policy_number: str, **kwargs) -> None:
        """Constructor method for Insurance class"""
        super().__init__(**kwargs)
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.policy_number = policy_number

    def to_dict(self) -> Dict:
        """Returns dictionary representation of object"""
        attr = super().to_dict()
        attr.update({
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "policy_number": self.policy_number,
        })
        return attr

    def __str__(self) -> str:
        """Returns string representation of object"""
        return f"[Insurance] ({self.id}) {self.to_dict()}"
