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
    
    def create_session(self):
        """ creates and returns a new session """
        if self.__session is None:
            self.__session = scoped_session(sessionmaker(bind=self.__engine))
        return self.__session

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def reload(self):
        """ Refreshes the session with the latest state of database """
        self.__session.close()
        Session = scoped_session(sessionmaker(bind=self.__engine))
        self.__session = Session()

    def create(self, model, **kwargs):
        if model not in self.__classes:
            raise ModelNotFoundError(model)
        obj = self.__classes[model](**kwargs)
        self.__session.add(obj)
        self.__session.commit()
        return obj

    def get(self, model, obj_id):
        if model not in self.__classes:
            raise ModelNotFoundError(model)
        query = self.__session.query(self.__classes[model]).filter_by(id=obj_id)
        obj = query.first()
        if obj is None:
            raise InstanceNotFoundError(obj_id, model)
        return obj

    def delete(self, model, obj_id):
        if model not in self.__classes:
            raise ModelNotFoundError(model)
        obj = self.__session.query(self.__classes[model]).filter_by(id=obj_id).first()
        if obj is None:
            raise InstanceNotFoundError(obj_id, model)
        self.__session.delete(obj)
        self.save()

    def all(self, model=None):
        """ Return all objects in the storage """
        objs = {}
        if model:
            query = self.__session.query(self.__classes[model])
            for obj in query.all():
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                objs[key] = obj
        else:
            for model in self.__classes:
                query = self.__session.query(self.__classes[model])
                for obj in query.all():
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    objs[key] = obj
        return objs

    def count(self, model=None):
        if model:
            return self.__session.query(model).count()
        else:
            count = 0
            for model in self.__classes:
                count += self.__session.query(model).count()
            return count

    def update(self, model, id, updates):
        if model not in self.__classes:
            raise ModelNotFoundError(model)
        obj = self.__session.query(self.__classes[model]).filter_by(id=id).first()
        if obj is None:
            raise InstanceNotFoundError(id, model)
        for field, value in updates.items():
            if field not in ('id', 'created_at', 'updated_at'):
                setattr(obj, field, value)
        obj.updated_at = datetime.utcnow()
        self.__session.commit()
