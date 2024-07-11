# address_routes.py
# This file defines the API endpoints for handling customer service requests.

from flask import request, jsonify
from main import app
from address_services import process_address_change_request

@app.route('/change-address', methods=['POST'])
def change_address():
    """
    Endpoint to handle address change requests.
    Receives JSON data from the mobile application and forwards it to the service layer for processing.
    """
    data = request.get_json()
    response = process_address_change_request(data)
    return jsonify(response)
