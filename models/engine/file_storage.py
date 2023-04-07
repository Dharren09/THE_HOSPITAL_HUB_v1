#!/bin/usr/python3
import models
from models.parent_model import ParentModel
import os
from models.patients import Patient
from models.staff import Staff
from models.pharmacy import Pharmacy
from models.billing_and_payment import BillingInvoice
from models.TeleHealth import TeleHealth
import json
from datetime import datetime

classes = {"Patient": Patient, "TeleHealth": TeleHealth, "Pharmacy": Pharmacy,
           "BillingInvoice": BillingInvoice, "Staff": Staff}


class FileStorage:
    """ This provides a simple file-based database system for storing
    and retrieving objects in a persistent way """

    # class private variables
    __objects: dict = {}
    __file_path: str = "file.json"

    def save(self):
        """ saves the objects to the file """
        all_objects = []
        for value in self.__objects.values():
            all_objects.append(value.to_dict())

        with open(self.__file_path, "w") as f:
            json.dump(all_objects, f)

    def reload(self):
        """ Refreshes the storage with the latest state of the file """
        try:
            all_objects = []

            with open(self.__file_path, "r") as f:
                all_objects = json.load(f)

            for obj in all_objects:
                key = obj["__class__"] + "." + obj["id"]
                value = eval(obj["__class__"])(**obj)
                self.__objects[key] = value
            return self.__objects
        except Exception as e:
            print(e)
            pass

    def all(self, cls=None):
        """ Returns the dictionary containing all objects of a certain class
        or all objects is no class is specified """
        if cls:
            class_dict = {}
            for key, value in self.__objects.items():
                class_name = value.__class__.__name__
                if cls == class_name:
                    class_dict[key] = value
            return class_dict
        return self.__objects

    def create(self, obj):
        """ Create a new object and add it to the storage """
        class_name = obj.__class__.__name__
        if class_name in classes:
            key = class_name + "." + obj.id
            self.__objects[key] = obj

    def get(self, cls, obj_id):
        """ Retrieve an object by its id """
        for key in self.all(cls).keys():
            only_id = key.split(".")[1]
            if obj_id == only_id:
                # Instantiates the object and then returns it
                return eval(cls)(**self.__objects[key].to_dict())
        return None

    def delete(self, obj):
        """ delete an object from storage by its id"""
        obj_id = obj.__class__.__name__ + "." + obj.id
        if obj_id in self.__objects:
            del self.__objects[obj_id]
            self.save()

    def update(self, obj, **kwargs):
        """Updates an instance"""
        try:
            obj_id = obj.__class__.__name__ + "." + obj.id
            if obj_id in self.__objects and kwargs:
                obj_dict = obj.to_dict()
                obj_dict.update(**kwargs)
                obj = eval(obj_dict["__class__"])(**obj_dict)
                self.create(obj)
                self.save()
        except Exception:
            pass
