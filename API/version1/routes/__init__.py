#!/usr/bin//python3

from flask import Flask, Blueprint
from .routes.patients import patients_bp
from .routes.pharmacy import pharmacy_bp
from .routes.staff import staff_bp
from .routes.billings_and_payments import BillingInvoice_bp
from .routes.TeleHealth import Telehealth_bp


api_bp = Blueprint('api', __name__)
api_bp.register_blueprint(patients_bp)
api_bp.register_blueprint(staff_bp)
api_bp.register_blueprint(pharmacy_bp)
api_bp.register_blueprint(BillingInvoice_bp)
api_bp.register_blueprint(Telehealth_bp)
