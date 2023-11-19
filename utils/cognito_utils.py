import base64
import hashlib
import hmac

def calculate_secret_hash(app_client_secret: str, app_client_id: str, username: str) -> str:
    """
    Calculates the SecretHash required for certain Cognito operations.

    Parameters:
        - app_client_secret (str): The client secret associated with the Cognito app client.
        - app_client_id (str): The app client ID associated with the Cognito user pool.
        - username (str): The username (email) of the user.

    Returns:
        - str: The calculated SecretHash.
    """
    message = bytes(username + app_client_id, 'utf-8')
    key = bytes(app_client_secret, 'utf-8')
    secret_hash = base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest()).decode('utf-8')
    return secret_hash
