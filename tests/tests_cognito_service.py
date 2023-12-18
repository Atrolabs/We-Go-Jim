import unittest
from unittest.mock import MagicMock, patch
from ..services.cognito_service import CognitoService


class TestCognitoService(unittest.TestCase):

    @patch('cognito_service.boto3.client')
    def setUp(self, mock_boto_client):
        # Replace 'your_module' with the actual module name where CognitoService is defined
        self.services.cognito_service = CognitoService()
        self.mock_cognito_client = MagicMock()
        mock_boto_client.return_value = self.mock_cognito_client

    def test_register_user_success(self):
        email = "user@example.com"
        password = "password123"
        user_type = "Student"

        # Mock the sign_up method of the Cognito client
        self.mock_cognito_client.sign_up.return_value = {'Some': 'Response'}

        response = self.cognito_service.register_user(email, password, user_type)

        self.assertEqual(response, {'Some': 'Response'})
        self.mock_cognito_client.sign_up.assert_called_once()

    def test_register_user_failure(self):
        email = "user@example.com"
        password = "password123"
        user_type = "Student"

        # Mock an exception being raised in sign_up
        self.mock_cognito_client.sign_up.side_effect = Exception("Some error")

        with self.assertRaises(Exception):
            self.cognito_service.register_user(email, password, user_type)

    def test_login_user_success(self):
        email = "user@example.com"
        password = "password123"

        # Mock the sign_in method of the Cognito client
        self.mock_cognito_client.sign_in.return_value = {'Some': 'Response'}

        response = self.cognito_service.login_user(email, password)

        self.assertEqual(response, {'Some': 'Response'})
        self.mock_cognito_client.sign_in.assert_called_once()

    def test_login_user_failure(self):
        email = "user@example.com"
        password = "password123"

        # Mock an exception being raised in sign_in
        self.mock_cognito_client.sign_in.side_effect = Exception("Some error")

        with self.assertRaises(Exception):
            self.cognito_service.login_user(email, password)

if __name__ == '__main__':
    unittest.main()
