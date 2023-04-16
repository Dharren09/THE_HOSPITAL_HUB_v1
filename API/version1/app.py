#!/usr/bin/python3

"""
Module is entry point to TheHospitalHub API
"""

from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from
from models import storage
from api.version1.views import ui

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Configure Swagger documentation
app.config['SWAGGER'] = {
    'title': 'TheHospitalHub API',
    'uiversion': 3
}
swagger = Swagger(app)

# Handle 404 errors
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

# Close database connection after request is finished
@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
