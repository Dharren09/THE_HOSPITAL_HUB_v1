#!/usr/bin/python3

from flask import Flask, Blueprint, render_template, jsonify, make_response, request
from models import storage, storage_env
from models.pharmacy import Pharmacy
from models.parent_model import ParentModel


#create blueprint
pharmacy_bp = Blueprint('pharmacy', __name__)

#create REST API for the blueprint
api = Api(pharmacy_bp)

@pharmacy_bp.route("/pharmacy", methods=["GET", "POST"])
@pharmacy_bp.route("/pharmacy/<string:pharmacy_id>", methods=["GET", "PUT", "DELETE"])

def pharmacy(drug_id=None):
    """Handles all default RESTful API actions for Drug class"""
    if pharmacy_id:
        equipment = storage.get("Pharmacy", pharmacy_id)
        if equipment is None:
            abort(404)
            return

    if request.method == "GET":
        if pharmacy_id is None:
            all_equipments = [equipment.to_dict() for equipment in
                         storage.all("Equipment").values()]
            return jsonify(all_equipments)
        return jsonify(equipment)

    elif request.method == "POST":
        data = request.get_json()
        if data is None:
            return jsonify({"message": "Not valid json"})
        elif "name" not in data:
            return jsonify({"message": "Please specify the name"})
        elif "quantity" not in data:
            return jsonify({"message": "Please specify the quantity"})
        if data["price"] == "None" or data["price"] == "" or data["price"] == None:
            del data["price"]
        if data["quantity"] == "None" or data["quantity"] == "" or data["quantity"] == None:
            del data["quantity"]
        new_equipment = Equipment(**data)
        new_equipment.save()
        return make_response(jsonify({"message": "Successfully added new equipment"},
                                     new_equipment.to_dict()), 200)

    elif request.method == "PUT":
        data = request.get_json()
        if data is None:
            return jsonify({"message": "Not valid json"})
        if data["price"] == "None" or data["price"] == "" or data["price"] == None:
            del data["price"]
        if data["quantity"] == "None" or data["quantity"] == "" or data["quantity"] == None:
            del data["quantity"]
        for attr, value in data.items():
            if attr not in ["id", "created_at", "updated_at"]:
                setattr(drug, attr, value)
        drug.save()
        return make_response(jsonify({"message": "Successfully updated the equipment"},
                                     equipment.to_dict()), 201)

    elif request.method == "DELETE":
        equipment.delete()
        storage.save()
        return jsonify({})
