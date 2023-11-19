import boto3
from botocore.exceptions import ClientError
from config.config_loader import USER_POOL_ID, CLIENT_ID, APP_CLIENT_SECRET

class CognitoService:
    def __init__(self):
        """
        Initialize a CognitoService instance.
        """
        self.user_pool_id = USER_POOL_ID
        self.client_id = CLIENT_ID
        self.client_secret = APP_CLIENT_SECRET
        self.client = boto3.client('cognito-idp', region_name='eu-central-1')

    def register_user(self, email, password, user_type):
        """
        Register a new user in the Cognito User Pool.

        :param email: The email address for the new user.
        :param password: The password for the new user.
        :param user_type: The user type as a string.

        :return: If successful, returns a dictionary with user details.
                 If unsuccessful, raises an exception with an error message.
        """
        try:
            user_attributes = [{'Name': 'email', 'Value': email}, {'Name': 'user_type', 'Value': user_type}]
            
            response = self.client.sign_up(
                ClientId=self.client_id,
                Username=email,  # Use email as the username
                Password=password,
                UserAttributes=user_attributes
            )
            
            return response
        except ClientError as e:
            raise Exception(f"Error registering user: {e}")
