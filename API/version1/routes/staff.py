#!/usr/bin/python3

from flask import Flask, Blueprint, abort, jsonify, make_response, request
from models.parent_model import ParentModel
from models import storage, storage_env
from models.staff import Staff

#create blueprint
staff_bp = Blueprint('staff', __name__)

#create REST API for the blueprint
api = Api(staff_bp)

@staff_bp.route("/staff", methods=["GET", "POST"])
@staff_bp.route("/staff/<string:staff_id>", methods=["GET", "PUT", "DELETE"])

def staff(staff_id=None):
    """Handles all default RESTful API actions for staff object"""
    if staff_id:
        staff = storage.get("Staff", staff_id)
        if not staff:
            abort(404)
            return

    if request.method == "GET":
        if staff_id:
            return jsonify(staff.to_dict())
        all_staff = [obj.to_dict() for obj in
                        storage.all("Staff").values()]
        return jsonify(all_staff)

    elif request.method == "POST":
        if request.get_json() is None:
            return jsonify({"message": "Not valid json"})
        elif "name" not in request.get_json():
            return jsonify({"message": "name must be specified"})
        elif "gender" not in request.get_json():
            return jsonify({"message": "gender must be specified"})

        attr = request.get_json()
        if attr["contact"] == "None" or attr["contact"] == "":
            del attr["contact"]
        if attr["age"]  == "None" or attr["age"] == "" or attr["age"] == 0:
            del attr["age"]
        obj = Staff(**attr)
        obj.save()
        staff = storage.get("Patient", obj.id)
        return make_response(jsonify(staff.to_dict()), 201)

    elif request.method == "PUT":
        if request.get_json() is None:
            return jsonify({"message": "Not valid json"})
        attr = request.get_json()
        if attr["contact"] == "None" or attr["contact"] == "":
            del attr["contact"]
        if attr["age"] == "None" or attr["age"] == "" or attr["age"] == 0:
            del attr["age"]
        for key, value in attr.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(staff, key, value)
        staff.save()
        staff = storage.get("Staff", patient.id)
        return make_response(jsonify(staff.to_dict()), 200)

    elif request.method == "DELETE":
        staff.delete()
        storage.save()
        return (jsonify({}))
