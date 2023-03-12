import uuid
from datetime import datetime


class ParentModel:
    """Parent class that implements the common functions amonst all the models."""

    def __init__(self, *args, **kwargs):
        """Constructor method.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        # Check if the keyword arguments dictionary is not empty.
        if kwargs:
            # Loop through the keyword arguments dictionary.
            for key, value in kwargs.items():
                # If the key is not 'id', set an instance attribute with the key and value.
                if key != "id":
                    setattr(self, key, value)
            # If the 'created_at' key exists in the keyword arguments and the type is a string,
            # convert the string to a datetime object and set the instance attribute to the datetime object.
            if (kwargs.get("created_at") and type(self.created_at) is str):
                self.created_at = datetime.strptime(kwargs["created_at"],
                                                    "%Y-%m-%d %H:%M:%S")
            else:
                self.created_at = datetime.utcnow()

            # If the 'updated_at' key exists in the keyword arguments and the type is a string,
            # convert the string to a datetime object and set the instance attribute to the datetime object.
            if (kwargs.get("updated_at") and type(self.created_at) is str):
                self.updated_at = datetime.strptime(kwargs["created_at"],
                                                    "%Y-%m-%d %H:%M:%S")
            else:
                self.updated_at = datetime.utcnow()
            # If the 'id' key does not exist in the keyword arguments, set the instance attribute to a new uuid.
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
        else:
            # If the keyword arguments dictionary is empty, set the 'id' attribute to a new uuid and
            # set the 'created_at' and 'updated_at' attributes to the current UTC datetime.
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def to_dict(self):
        """Return a dictionary representation of the object."""
        # Create an empty dictionary to store the attributes of the object.
        attr = {}
        # Add the class name as a key-value pair to the dictionary.
        attr["__class__"] = self.__class__.__name__
        # Loop through the attributes of the object.
        for key, value in dict(self.__dict__).items():
            # If the attribute is the 'created_at' attribute, convert the datetime object to a string in the specified format.
            if key == "created_at":
                attr[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            # If the attribute is the 'updated_at' attribute, convert the datetime object to a string in the specified format.
            elif key == "updated_at":
                attr[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            # If the attribute is not the 'created_at' or 'updated_at' attribute, add it to the dictionary.
            else:
                attr[key] = value
        # Return the dictionary.
        return attr

    def __str__(self):
        """Return a string representation of the object."""
        # Return a string representation of the object with the class name, id, and dictionary representation of the object.
        return f"[[{self.__class__.__name__}] ({self.id}) {self.to_dict()}]"
