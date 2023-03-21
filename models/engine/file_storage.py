#!/usr/bin/python3
"""
This File defines the storage system (File System)
For the project.
It uses json format to serialize or deserialize
an object """


import models
from models.parent_model import ParentModel
import os
from models.patients import Patient
from models.staff import Staff
from models.pharmacy import Pharmacy
from models.billing_and_payment import BillingInvoice
from models.TeleHealth import TeleHealth
import json
from json.decoder import JSONDecodeError
from datetime import datetime



class FileStorage:
    """ This provides a simple file-based database system for storing 
    and retrieving objects in a persistent way """

    # class private variables
    __objects: dict = {}
    __file_path: str = "file.json"
    __classes = {"Patient": Patient, "TeleHealth": TeleHealth, "Pharmacy": Pharmacy,
                 "BillingInvoice": BillingInvoice, "Staff": Staff}

    def all(self, model=None):
        """ Returns the dictionary containing all objects of a certain class
        or all objects is no class is specified """
        if model is None:
            return FileStorage.__objects
        else:
            if isinstance(model, str):
                model = globals()[model]
            return {k: v for k, v in FileStorage.__objects.items()
                    if isinstance(v, model)}

    def new(self, obj):
        """ Stores a new Object in the storage dictionary """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj.to_dict()

    def save(self):
        """ saves the objects to the file """
        with open(FileStorage.__file_path, "w") as f:
            json.dump(FileStorage.__objects, f)

    def reload(self):
        """ Refreshes the storage with the latest state of the file """
        try:
            with open(FileStorage.__file_path, "r") as f:
                FileStorage.__objects = json.load(f)
        except FileNotFoundError:
            pass

    def create(self, model, **kwargs):
        """ Create a new object and add it to the storage """
        model = globals().get(model)
        if model:
            obj = model(**kwargs)
            self.new(obj)
            self.save()
            return obj
        else:
            return None

    def get(self, model, obj_id):
        """ Retrieve an object by its id """
        cls = globals().get(model)
        if cls:
            key = "{}.{}".format(cls.__name__, obj_id)
            obj_dict = FileStorage.__objects.get(key)
            if obj_dict:
                return cls(**obj_dict)
        return None

    def delete(self, obj_id):
        """ delete an object from storage by its id"""
        key = "{}.{}".format(obj_id.__class__.__name__, obj_id)
        del FileStorage.__objects[key]
        self.save()
 
    def count(self, model=None):
        """ Count the number of objects of a certain class
        or all objects if no class is specified """
        if model is None:
            return len(FileStorage.__objects)
        else:
            if isinstance(model, str):
                cls = globals().get(model)
            return sum(1 for v in FileStorage.__objects.values()
                       if v['__class__'] == cls.__name__)

    def update(self, obj, updates):
        """Updates an instance"""
        for field, value in updates.items():
            if isinstance(getattr(obj,field, None), property):
                setattr(obj, field, value)
                obj_dict = obj.to_dict()
                obj_dict['updated_at'] = datetime.utcnow().isoformat()
                FileStorage.__objects["{}.{}".format(obj.__class__.__name__, obj.id)] = obj_dict
        self.save()
