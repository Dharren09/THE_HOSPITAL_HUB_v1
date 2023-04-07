#!/usr/bin/python3
"""
Contains the class DBStorage
"""


import models
from models.parent_model import ParentModel, Base
from models.patients import Patient
from models.staff import Staff
from models.pharmacy import Pharmacy
from models.billing_and_payment import BillingInvoice
from models.TeleHealth import TeleHealth
import json
from json.decoder import JSONDecodeError
from datetime import datetime
from sqlalchemy import create_engine
from os import getenv
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker



class DBStorage:
    """ class interacts with mysql database """
    __engine = None
    __session = None
    __classes = {"Patient": Patient, "Pharmacy": Pharmacy, "TeleHealth": TeleHealth,
                 "BillingInvoice": BillingInvoice, "Staff": Staff}

    def __init__(self):
        """ Instantiates a DBStorage object """
        db_user = getenv('HH_USER')
        db_pwd = getenv('Dharrenz')
        db_host = getenv('localhost')
        db_name = getenv('TheHospitalHub')
        db_env = getenv('storage_ENV')
        self.__engine = create_engine(f"mysql+mysqldb://{db_user}:{db_pwd}@{db_host}/{db_name}")
        
        if db_env == "test":
            Base.metadata.drop_all(self.__engine)
    
    def create(self, obj):
        """ creates and returns a new object """
        self.__session.add(obj)

    def save(self):
        """ saves to database """
        self.__session.commit()

    def reload(self):
        """ Refreshes the session with the latest state of database """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def get(self, model, obj_id):
        for key in self.all(model).keys():
            oid = key.split(".")[1]
            if obj_id == oid:
                obj = self.__session.query(__classes[model]).get(oid)
                return obj
        return None

    def delete(self, obj):
        self.__session.delete(obj)
        self.__session.commit()

    def all(self, model=None):
        """ Return all objects in the storage """
        if model:
            objs = {}
            class_objs = self.__session.query(__classes[model]).all()
            for obj in class_objs:
                key = obj.__class__.__name__ + "." + obj.id
                objs[key] = obj
            return objs

        all_objects = {}

        for model in __classes:
            objs = self.__session.query(__classes[model]).all()
            for obj in objs:
                key = obj.__class__.__name__ + "." + obj.id
                all_objects[key] = obj
        return all_objects

    def count(self, model=None):
        if model:
            return len(self.all(model))
        return len(self.all())

    def update(self, key, **kwargs):
        obj_id = key.split(".")[1]
        class_name = key.split(".")[0]
        obj = self.__session.query(__classes[class_name
                                           ]).filter_by(id=obj_id).first()
        for key, value in kwargs.items():
            setattr(obj, key, value)
        self.__session.commit()

    def close(self):
        """Closes transaction"""
        self.__session.close()
