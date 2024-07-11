import unittest
from unittest.mock import patch, MagicMock
from address_services import process_address_change_request, call_internal_api, forward_to_camunda

class AddressServicesTestCase(unittest.TestCase):

    @patch('address_services.requests.post')
    def test_call_internal_api_success(self, mock_post):
        # Mock the requests.post to return a successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': True}
        mock_post.return_value = mock_response

        data = {'user_id': '12345', 'old_address': '123 Old St', 'new_address': '456 New St'}
        response = call_internal_api(data)

        self.assertEqual(response, {'status': True})
        mock_post.assert_called_once_with('https://internal.api/control-check', json=data)

    @patch('address_services.requests.post')
    def test_call_internal_api_failure(self, mock_post):
        # Mock the requests.post to return a failure response
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': False}
        mock_post.return_value = mock_response

        data = {'user_id': '12345', 'old_address': '123 Old St', 'new_address': '456 New St'}
        response = call_internal_api(data)

        self.assertEqual(response, {'status': False})
        mock_post.assert_called_once_with('https://internal.api/control-check', json=data)

    @patch('address_services.requests.post')
    def test_forward_to_camunda_success(self, mock_post):
        # Mock the requests.post to return a successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'success', 'workflow_id': '123'}
        mock_post.return_value = mock_response

        data = {'user_id': '12345', 'old_address': '123 Old St', 'new_address': '456 New St'}
        response = forward_to_camunda(data)

        self.assertEqual(response, {'status': 'success', 'workflow_id': '123'})
        mock_post.assert_called_once_with('https://camunda.api/workflow', json=data)

    @patch('address_services.requests.post')
    def test_forward_to_camunda_failure(self, mock_post):
        # Mock the requests.post to return a failure response
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'failure', 'error': 'Invalid data'}
        mock_post.return_value = mock_response

        data = {'user_id': '12345', 'old_address': '123 Old St', 'new_address': '456 New St'}
        response = forward_to_camunda(data)

        self.assertEqual(response, {'status': 'failure', 'error': 'Invalid data'})
        mock_post.assert_called_once_with('https://camunda.api/workflow', json=data)

    @patch('address_services.call_internal_api')
    @patch('address_services.forward_to_camunda')
    def test_process_address_change_request_success(self, mock_forward_to_camunda, mock_call_internal_api):
        # Mock the control check and Camunda workflow to return success
        mock_call_internal_api.return_value = {'status': True}
        mock_forward_to_camunda.return_value = {'status': 'success', 'workflow_id': '123'}

        data = {'user_id': '12345', 'old_address': '123 Old St', 'new_address': '456 New St'}
        response = process_address_change_request(data)

        self.assertEqual(response, {'status': 'success', 'workflow_id': '123'})
        mock_call_internal_api.assert_called_once_with(data)
        mock_forward_to_camunda.assert_called_once_with(data)

    @patch('address_services.call_internal_api')
    @patch('address_services.forward_to_camunda')
    def test_process_address_change_request_control_check_failed(self, mock_forward_to_camunda, mock_call_internal_api):
        # Mock the control check to fail
        mock_call_internal_api.return_value = {'status': False}

        data = {'user_id': '12345', 'old_address': '123 Old St', 'new_address': '456 New St'}
        response = process_address_change_request(data)

        self.assertEqual(response, {'error': 'Control check failed'})
        mock_call_internal_api.assert_called_once_with(data)
        mock_forward_to_camunda.assert_not_called()

if __name__ == '__main__':
    unittest.main()
