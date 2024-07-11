import unittest
from unittest.mock import patch, MagicMock
from main import app

class AddressRoutesTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('address_routes.process_address_change_request')
    def test_change_address_success(self, mock_process_request):
        # Mock the process_address_change_request function to return a successful response
        mock_process_request.return_value = {'status': 'success', 'message': 'Address change processed'}

        # Create a sample payload
        payload = {
            'user_id': '12345',
            'old_address': '123 Old St',
            'new_address': '456 New St'
        }

        # Send a POST request to the /change-address endpoint
        response = self.app.post('/change-address', json=payload)

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'success', 'message': 'Address change processed'})

    @patch('address_routes.process_address_change_request')
    def test_change_address_control_check_failed(self, mock_process_request):
        # Mock the process_address_change_request function to return a failure response
        mock_process_request.return_value = {'error': 'Control check failed'}

        # Create a sample payload
        payload = {
            'user_id': '12345',
            'old_address': '123 Old St',
            'new_address': '456 New St'
        }

        # Send a POST request to the /change-address endpoint
        response = self.app.post('/change-address', json=payload)

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'error': 'Control check failed'})

if __name__ == '__main__':
    unittest.main()
