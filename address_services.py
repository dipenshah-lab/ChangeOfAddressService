# address_services.py
# This file contains the logic for processing requests, including control checks and forwarding to Camunda.

import requests

def call_internal_api(data):
    """
    Simulate a call to an internal system API for a control check.
    """
    # Replace with actual internal API endpoint and logic
    response = requests.post('https://internal.api/control-check', json=data)
    return response.json()

def forward_to_camunda(data):
    """
    Simulate forwarding the request to a Camunda workflow.
    """
    # Replace with actual Camunda API endpoint and logic
    response = requests.post('https://camunda.api/workflow', json=data)
    return response.json()

def process_address_change_request(data):
    """
    Process the address change request.
    1. Call the internal system API for a control check.
    2. Forward the request to the Camunda workflow if the control check passes.
    """
    control_check = call_internal_api(data)
    if not control_check['status']:
        return {'error': 'Control check failed'}
    camunda_response = forward_to_camunda(data)
    return camunda_response
