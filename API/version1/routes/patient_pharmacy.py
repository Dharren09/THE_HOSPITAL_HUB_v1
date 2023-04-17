#!/usr/bin/python3

from flask import Flask, Blueprint, abort, jsonify, make_response, request
from models.parent_model import ParentModel
from models import storage, storage_ENV
from models.patients import Patient
from models.pharmacy import Pharmacy
from models.patients import Patient
from API.version1.routes import api_bp

#create blueprint
patient-pharmacy_bp = Blueprint('patient_pharmacy', __name__)

#create REST API for the blueprint
api = Api(patient-pharmacy_bp)

@ui.route("/patient/<string:patient_id>/pharmacy", methods=["GET"])
@ui.route("/patient/<string:patient_id>/pharmacy/<string:pharmacy_id>", methods=["POST", "DELETE"])
def patient_drug(patient_id, pharmacy_id=None):
    """Handles all default api actions for patients_drugs relationship"""
    if patient_id is None:
        return

    patient = storage.get("Patient", patient_id)
    if patient is None:
        abort(404)
        return

    if pharmacy_id:
        equipment = storage.get("Drug", pharmacy_id)
        if equipment is None:
            abort(404)
            return

    patient = storage.get("Patient", patient_id)

    patient_pharmacy = patient.pharmacy

    if request.method == "GET":
        return jsonify([pharmacy.to_dict() for equipment in patient_pharmacy])

    elif request.method == "POST":
        if equipment in patient_pharmacy:
            equipment.quantity -= 1
            patient_pharmacy.append(equipment)
            pharmacy.save()
            patient.save()
            equpiment = storage.get("Pharmacy", pharmacy_id)
            return jsonify(equipment.to_dict())
        patient_pharmacy.append(equipment)
        equipment.quantity -= 1
        pharmacy.save()
        patient.save()
        equipment = storage.get("Pharmacy", pharmacy_id)
        return jsonify(equipment.to_dict())

    elif request.method == "DELETE":
        patient_pharmacy.remove(equipment)
        storage.save()
        return jsonify({})
