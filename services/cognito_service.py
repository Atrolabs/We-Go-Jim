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


    def get_user_attrib_by_sub(self, user_sub, attribute_type):
        """
        Retrieves a specific attribute of a user based on their sub (subject) identifier.

        Parameters:
            - user_sub (str): The sub (subject) identifier of the user.
            - attribute_type (str): The type of attribute to retrieve.

        Returns:
            - Union[str, None]: The value of the specified attribute, or None if the attribute is not found.

        Example:
            ```python
            cognito_service = CognitoService()
            attribute_value = cognito_service.get_user_attrib_by_sub(user_sub="user123", attribute_type="email")
            print(attribute_value)
            ```

        Note:
            Make sure to handle exceptions appropriately when calling this method.
        """
        try:
            # Get the user details using admin_get_user
            response = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=user_sub
            )

            # Extract the specified attribute from the response
            attribute_value = None
            for attribute in response['UserAttributes']:
                if attribute['Name'] == attribute_type:
                    attribute_value = attribute['Value']
                    break  # Stop searching once the attribute is found

            return attribute_value

        except Exception as e:
            print(f"Error: {e}")
            return None
        

        
    def get_sub_by_email(self, email):
        """
        Retrieves the sub (subject) identifier of a user based on their email address.

        Parameters:
            - email (str): The email address of the user.

        Returns:
            - Union[str, None]: The sub (subject) identifier of the user, or None if the user is not found.

        Example:
            ```python
            cognito_service = CognitoService()
            sub_value = cognito_service.get_sub_by_email(email="user@example.com")
            print(sub_value)
            ```

        Note:
            Make sure to handle exceptions appropriately when calling this method.
        """

        try:
            # Use admin_get_user to get user attributes, including sub
            response = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=email
            )

            # Extract user sub (subject)
            for attribute in response['UserAttributes']:
                if attribute['Name'] == 'sub':
                    return attribute['Value']

            return None  # sub not found

        except Exception as e:
            print(f"Error: {e}")
            return None


    
    def check_user_exists(self, user_sub):
        """
        Checks whether a user with the specified sub (subject) identifier exists.

        Parameters:
            - user_sub (str): The sub (subject) identifier of the user.

        Returns:
            - bool: True if the user exists, False otherwise.

        Example:
            ```python
            cognito_service = CognitoService()
            user_exists = cognito_service.check_user_exists(user_sub="user123")
            print(user_exists)
            ```

        Note:
            Make sure to handle exceptions appropriately when calling this method.
        """
        try:
            response = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=user_sub
            )
            return True  # User exists
        except self.client.exceptions.UserNotFoundException:
            return False  # User not found
