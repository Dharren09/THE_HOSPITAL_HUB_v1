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

@telehealth_bp.route("/telehealth", methods=["GET", "POST"])
def create_telehealth_activity():
    if request.method == "GET":
        # Return all telehealth logs and schedules
        telehealth_logs = [obj.to_dict() for obj in storage.all("TeleHealth").values()]
        telehealth_schedules = [obj.to_dict() for obj in storage.all("TeleHealthSchedule").values()]
        return jsonify({"telehealth_logs": telehealth_logs, "telehealth_schedules": telehealth_schedules})

    elif request.method == "POST":
        # Create a new telehealth activity
        data = request.get_json()
        patient_id = data.get("patient_id")
        duration = data.get("duration")
        notes = data.get("notes")
        
        if not patient_id:
            return jsonify({"message": "Patient ID must be specified."}), 400
        if not duration:
            return jsonify({"message": "Duration must be specified."}), 400
        
        patient = storage.get("Patient", patient_id)
        if not patient:
            return jsonify({"message": f"Patient with ID {patient_id} not found."}), 404
        
        telehealth = TeleHealth(patient=patient, duration=duration, notes=notes)
        telehealth.save()
        
        return make_response(jsonify(telehealth.to_dict()), 201)

@telehealth_bp.route("/telehealth/<string:telehealth_id>", methods=["PUT", "DELETE"])
def modify_or_delete_telehealth_activity(telehealth_id):
    telehealth = storage.get("TeleHealth", telehealth_id)
    if not telehealth:
        abort(404)
    
    if request.method == "PUT":
        # Update an existing telehealth activity
        data = request.get_json()
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(telehealth, key, value)
        telehealth.save()
        return make_response(jsonify(telehealth.to_dict()), 200)
    
    elif request.method == "DELETE":
        # Delete an existing telehealth activity
        telehealth.delete()
        storage.save()
        return jsonify({"message": "Telehealth activity deleted."})
