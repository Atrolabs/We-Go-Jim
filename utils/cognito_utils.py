import base64
import hashlib
import hmac
import jwt
from functools import wraps
from flask import redirect, url_for, session
from config.config_loader import USER_POOL_ID


def calculate_secret_hash(app_client_secret: str, app_client_id: str, username: str) -> str:
    """
    Calculates the SecretHash required for certain Cognito operations.

    Parameters:
        - app_client_secret (str): The client secret associated with the Cognito app client.
        - app_client_id (str): The app client ID associated with the Cognito user pool.
        - username (str): The username (email) of the user.

    Returns:
        - str: The calculated SecretHash.

    Example:
    ```python
    app_client_secret = "your_client_secret"
    app_client_id = "your_client_id"
    username = "user@example.com"

    # Calculate the SecretHash
    secret_hash = calculate_secret_hash(app_client_secret, app_client_id, username)

    # Print the result
    print(f"The calculated SecretHash for user {username} is: {secret_hash}")
    ```
    """
    message = bytes(username + app_client_id, 'utf-8')
    key = bytes(app_client_secret, 'utf-8')
    secret_hash = base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest()).decode('utf-8')
    return secret_hash


def decode_cognito_jwt(token: str) -> dict:
    """
    Decodes a JWT token issued by Amazon Cognito for a user in the specified user pool.

    Parameters:
        - token (str): The JWT token to be decoded.

    Returns:
        - dict: A dictionary containing the decoded information from the JWT token.

    Note:
    This function performs the decoding without verifying the signature, expiration, issuance time,
    or audience. It is intended for scenarios where these verifications are handled separately or skipped
    for specific reasons. Ensure that proper precautions are taken when using this function in your application.

    Example:
    ```python
    token = "eyJhbGciOiJSUzI1NiIsInR5CI6IkpXVCJ9..."
    decoded_token = decode_cognito_jwt(token)
    print(decoded_token)
    ```

    Important:
    The use of this function may expose your application to security risks if not used carefully.
    Always ensure that appropriate security measures are in place when disabling signature and other verifications.

    """
    issuer = f'https://cognito-idp.eu-central-1.amazonaws.com/{USER_POOL_ID}'
    decoded_token = jwt.decode(
        token,
        verify=False,
        options={
            'verify_signature': False,
            'verify_exp': False,
            'verify_iat': False,
            'verify_aud': False,
            'iss': issuer
        }
    )
    return decoded_token


def login_required(route_function):
    @wraps(route_function)
    def protected_route(*args, **kwargs):
        # Check if user is logged in (you can customize this condition based on your authentication logic)
        if 'user_sub' in session:
            return route_function(*args, **kwargs)
        else:
            # Redirect to the login page if not logged in
            return redirect(url_for('login.login'))

    return protected_route
    