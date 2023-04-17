#!/usr/bin/python3

from flask import Flask, Blueprint, abort, jsonify, make_response, request
from models.parent_model import ParentModel
from models import storage, storage_env
from flask_restful import Api, Resource
from models.billings_and_payments import BillingInvoice

#create blueprint
BillingInvoice_bp = Blueprint('BillingInvoice', __name__)

#create REST API for the blueprint
api = Api(BillingsInvoice_bp)

@billings_bp.route("/BillingInvoice/<string: patientt_id>", methods=["GET", "POST"])
@billings_bp.route("/BillingInvoice/<string:BillingInvoice_id>", methods=["GET", "PUT", "DELETE"])
def BillingInvoice(BillingInvoice_id=None, patient_id=None):
    """Handles all default RESTful API actions for Payment class"""
    if BillingInvoice_id:
        payment = storage.get("BillingInvoice", BillingInvoice_id)
        if payment is None:
            abort(404)
            return
    if patient_id:
        patient = storage.get("Patient", patient_id)
        if patient is None:
            abort(404)
            return

    if request.method == "GET":
        if BillingInvoice_id is None:
            all_payments = [payment.to_dict() for payment in
                            storage.all("Payment").values()]
            return jsonify(all_payments)
        return jsonify(payment.to_dict())

    elif request.method == "POST":
        data = request.get_json()
        if data is None:
            return jsonify({"message": "Not valid JSON"})
        elif "amount" not in data:
            return jsonify({"message": "Please specify amount"})
        if data["paid"] == "None" or data["paid"] == "" or data["paid"] == 0:
            data["paid"] = 0
        data["patient_id"] = patient.id
        new_payment = Payment(**data)
        new_payment.save()
        pay = storage.get("Payment", new_payment.id)
        return make_response(jsonify({"message": "successfully added"},
                                     pay.to_dict(), 201))

    elif request.method == "PUT":
        data = request.get_json()
        if data is None:
            return jsonify({"message": "Not valid JSON"})
        for attr, value in data.items():
            if attr not in ["id", "created_at", "updated_at"]:
                setattr(payment, attr, value)
        payment.save()
        return make_response(jsonify({"message": "successfully updated"},
                                     payment.to_dict(), 200))

    elif request.method == "DELETE":
        payment.delete()
        storage.save()
        return jsonify({})
