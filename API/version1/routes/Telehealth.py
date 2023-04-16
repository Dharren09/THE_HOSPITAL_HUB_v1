#!/usr/bin/python3

from flask import Flask, Blueprint, abort, jsonify, make_response, request
from flask_restful import Api, Resource
from models.telehealth import TeleHealth
from models.patients import Patient
from models import storage, storage_env
from datetime import datetime

#create blueprint
telehealth_bp = Blueprint('telehealth', __name__)

#create REST API for the blueprint
api = Api(telehealth_bp)
