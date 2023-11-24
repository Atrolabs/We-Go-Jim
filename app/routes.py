from flask import Blueprint, render_template, request, jsonify, session
from services.cognito_service import CognitoService 
from typing import Union, Dict

# Define Flask Blueprints for different parts of the application
home_bp = Blueprint("home", __name__)
login_bp = Blueprint("login", __name__)
register_bp = Blueprint("register", __name__)

# Create an instance of CognitoService to interact with Amazon Cognito
cognito_service = CognitoService()  

@home_bp.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@login_bp.route('/login', methods=['GET', 'POST'])
def login() -> Union[str, Dict[str, Union[bool, str]]]:
    """
    Render the login page for `GET` requests and handle user login for POST requests.

    Returns:
        - For `GET` requests, returns the rendered `HTML` template for the login page.
        - For `POST` requests:
            - If login is successful, returns a `JSON` response indicating success.
            - If an error occurs during login, returns a `JSON` response indicating failure.

    Raises:
        Exception: If an unexpected error occurs during user login.

    Example:
        To render the login page:
        ```python
        result = login()  # GET request
        ```

        To handle user login:
        ```python
        data = {
            'email': 'user@example.com',
            'password': 'Password#123',
        }
        result = login(request_data=data)  # POST request
        ```

    Note:
        - This function expects `JSON` data for `POST` requests. The `JSON` should contain 'email' and 'password' keys.
    """
    if request.method == 'POST':
        try:
            data = request.json
            email = data.get('email')
            password = data.get('password')

            # Call your CognitoService method for login here
            response = cognito_service.login_user(email, password)

            # Note: For debugging purposes only. Remove the following line in production.
            print(response)

            # Check if the Cognito response indicates a successful login
            if 'AuthenticationResult' in response:
                access_token = response['AuthenticationResult']['AccessToken']
                print(access_token)
                # Set up user session (example)
                session['access_token'] = access_token

                # Uncomment the next line to make the session permanent
               # session.permanent = True

                # Return a success message
                return jsonify({'success': True, 'message': 'User logged in successfully'})
            
            # Handle login failure with a specific error message
            return jsonify({'success': False, 'message': 'Login failed. Please check your credentials.'})
        
        # Handle other exceptions
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    return render_template("login.html")


@register_bp.route('/register', methods=['GET', 'POST'])
def register() -> Union[str, Dict[str, Union[bool, str]]]:
    """
    Render the registration page for `GET` requests and handle user registration for POST requests.

    Returns:
        - For `GET` requests, returns the rendered `HTML` template for the registration page.
        - For `POST` requests:
            - If registration is successful, returns a `JSON` response indicating success.
            - If an error occurs during registration, returns a `JSON` response indicating failure.

    Raises:
        Exception: If an unexpected error occurs during user registration.

    Example:
          To render the registration page:
            ```python
            result = register()  # GET request
            ```

          To handle user registration:
            ```python
            data = {
                'email': 'user@example.com',
                'password1': 'Password#123',
                'isTrainer': False
            }
            result = register(request_data=data)  # POST request
            ```

    Note:
        - This function expects `JSON` data for `POST` requests. The `JSON` should contain 'email', 'password1', and 'isTrainer' keys.
        - The 'isTrainer' key indicates whether the user is a Trainer. If present and `True`, the `user_type` is set to 'Trainer'; otherwise, it's set to 'Student'.
    """
    if request.method == 'POST':
        try:
            data = request.json  # Use request.json to handle JSON data
            email = data.get('email')
            password = data.get('password1')
            user_type = 'Trainer' if data.get('isTrainer') else 'Student'

            response = cognito_service.register_user(email, password, user_type)

            # Note: For debugging purposes only. Remove the following line in production.
            print(response)
            
            # Handle register response
            return jsonify({'success': True, 'message': 'User registered successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    return render_template("register.html")
