import boto3
from botocore.exceptions import ClientError
from config.config_loader import USER_POOL_ID, APP_CLIENT_ID, APP_CLIENT_SECRET
from utils.cognito_utils import calculate_secret_hash

class CognitoService():
    """
    A class representing a service for interacting with Amazon Cognito for user registration and login.

Attributes:
    - user_pool_id (str): The ID of the Cognito user pool.
    - app_client_id (str): The app client ID associated with the Cognito user pool.
    - app_client_secret (str): The app client secret associated with the Cognito app client.
    - client (boto3.client): An instance of the Boto3 Cognito Identity Provider client.

Methods:
    - register_user(email: str, password: str, user_type: str) -> dict:
        Registers a new user in the Cognito user pool.

        Parameters:
            - email (str): The email address of the user.
            - password (str): The password for the user.
            - user_type (str): The type of the user.

        Returns:
            - dict: A dictionary containing the response from the Cognito service.

        Raises:
            - Exception: If an error occurs during user registration.

        Example:
            ```python
            cognito_service = CognitoService()
            response = cognito_service.register_user(email="user@example.com", password="password123", user_type="standard")
            print(response)
            ```

        Note:
            Make sure to handle exceptions appropriately when calling this method.

    - login_user(email: str, password: str) -> dict:
        Logs in a user with the provided credentials in the Cognito user pool.

        Parameters:
            - email (str): The email address of the user.
            - password (str): The password for the user.

        Returns:
            - dict: A dictionary containing the response from the Cognito service.

        Raises:
            - Exception: If an error occurs during user login.

        Example:
            ```python
            cognito_service = CognitoService()
            response = cognito_service.login_user(email="user@example.com", password="password123")
            print(response)
            ```

        Note:
            Make sure to handle exceptions appropriately when calling this method.
    """

    def __init__(self):
        """
        Initializes a new instance of the CognitoService class.
        """
        self.user_pool_id = USER_POOL_ID
        self.app_client_id = APP_CLIENT_ID
        self.app_client_secret = APP_CLIENT_SECRET
        self.client = boto3.client('cognito-idp', region_name='eu-central-1')

    def register_user(self, email: str, password: str, user_type: str) -> dict:
        """
        Registers a new user in the Cognito user pool.

        Parameters:
            - email (str): The email address of the user.
            - password (str): The password for the user.
            - user_type (str): The type of the user.

        Returns:
            - dict: A dictionary containing the response from the Cognito service.

        Raises:
            - Exception: If an error occurs during user registration.

        Example:
            ```python
            cognito_service = CognitoService()
            response = cognito_service.register_user(email="user@example.com", password="password123", user_type="Student")
            print(response)
            ```

        Note:
            Make sure to handle exceptions appropriately when calling this method.
        """
        try:
            user_attributes = [{'Name': 'email', 'Value': email}, {'Name': 'custom:user_type', 'Value': user_type}]

            secret_hash = calculate_secret_hash(APP_CLIENT_SECRET, APP_CLIENT_ID, email)
            
            response = self.client.sign_up(
                ClientId=self.app_client_id,
                SecretHash=secret_hash,  
                Username=email,  # Use email as the username
                Password=password,
                UserAttributes=user_attributes
            )
            return response
        except ClientError as e:
            raise Exception(f"Error registering user: {e}")

    def login_user(self, email: str, password: str) -> dict:
        """
        Logs in a user with the provided credentials in the Cognito user pool.

        Parameters:
            - email (str): The email address of the user.
            - password (str): The password for the user.

        Returns:
            - dict: A dictionary containing the response from the Cognito service.

        Raises:
            - Exception: If an error occurs during user login.

        Example:
            ```python
            cognito_service = CognitoService()
            response = cognito_service.login_user(email="user@example.com", password="password123")
            print(response)
            ```

        Note:
            Make sure to handle exceptions appropriately when calling this method.
        """
        try:
            secret_hash = calculate_secret_hash(APP_CLIENT_SECRET, APP_CLIENT_ID, email)

            response = self.client.initiate_auth(
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password,
                    'SECRET_HASH': secret_hash,
                },
                ClientId=self.app_client_id,
            )

            return response
        except ClientError as e:
            raise Exception(f"Error logging in user: {e}")


    def get_user_type(self, user_sub):
        try:
            # Get the user details using admin_get_user
            response = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=user_sub
            )
            # Extract custom attribute from the response
            custom_attribute_value = None
            for attribute in response['UserAttributes']:
                if attribute['Name'] == 'custom:user_type':  # Replace with your custom attribute name
                    custom_attribute_value = attribute['Value']

            return custom_attribute_value

        except Exception as e:
            print(f"Error: {e}")
            return None