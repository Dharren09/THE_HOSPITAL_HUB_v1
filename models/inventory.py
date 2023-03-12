from typing import Dict, Any, List
from parent_model import ParentModel


class Inventory(ParentModel):
    """Class representing the Inventory model"""
    def __init__(self, *args: List[Any], **kwargs: Dict[str, Any]):
        super().__init__(*args, **kwargs)
        self.name: str = kwargs.get('name', '')
        self.description: str = kwargs.get('description', '')
        self.quantity: int = kwargs.get('quantity', 0)
        self.price: float = kwargs.get('price', 0.0)
    
    @classmethod
    def get_all(cls) -> List:
        """
        Retrieves all inventory items.

        Returns:
            A list of all inventory items.
        """
        return session.query(cls).all()
    
    @classmethod
    def get_by_id(cls, inventory_id: str) -> "Inventory":
        """
        Retrieves an inventory item by ID.

        Args:
            inventory_id (str): The ID of the inventory item to retrieve.

        Returns:
            An instance of the Inventory class with the specified ID.
        """
        return session.query(cls).filter_by(id=inventory_id).first()

    def to_dict(self) -> Dict[str, Any]:
        """Returns a dictionary representation of the model"""
        inventory_dict = super().to_dict()
        inventory_dict.update({
            'name': self.name,
            'description': self.description,
            'quantity': self.quantity,
            'price': self.price,
        })
        return inventory_dict
