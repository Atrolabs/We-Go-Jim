from flask import Blueprint, render_template, request, jsonify, session
from services.cognito_service import CognitoService 
from typing import Union, Tuple
from utils.cognito_utils import decode_cognito_jwt, login_required
from utils.logs_utils import configure_logging, log_error
from services.s3_service import S3Service

configure_logging()

# Define Flask Blueprints for different parts of the applications
login_bp = Blueprint("login", __name__)
register_bp = Blueprint("register", __name__)
dashboard_bp = Blueprint("dashboard", __name__)

# Create an instance of CognitoService to interact with Amazon Cognito
cognito_service = CognitoService()  


@dashboard_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    """Render the dashboard page"""
    # Retrieve user_sub from the session
    user_sub = session.get('user_sub') 
    user_type = session.get('user_type')
    return render_template('dashboard.html', user_sub=user_sub, user_type=user_type)



@login_bp.route('/login', methods=['GET', 'POST'])
def login() -> Union[str, Tuple[str, int]]:
    """
    Render the login page for `GET` requests and handle user login for POST requests.

    Returns:
        - For `GET` requests, returns the rendered `HTML` template for the login page.
        - For `POST` requests:
            - If login is successful, returns a `JSON` response indicating success with a status code of `200`.
            - If an error occurs during login, returns a `JSON` response indicating failure with a status code of `400`.

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

            # Check if the Cognito response indicates a successful login
            if 'AuthenticationResult' in response:
                access_token = response['AuthenticationResult']['AccessToken']
                decoded_token = decode_cognito_jwt(access_token)
                user_sub = decoded_token.get('sub')
                user_type = cognito_service.get_user_type(user_sub)


                # Set up user session
                session['user_sub'] = user_sub
                session['user_type'] = user_type

                # Return a success message
                return jsonify({'success': True, 'message': 'User logged in successfully'}), 200
            
            # Handle login failure with a specific error message
            return jsonify({'success': False, 'message': 'Incorrect username or password.'}), 400
        
        # Catch any exception and log it
        except Exception as e:
            log_error(str(e))
            return jsonify({'success': False, 'message': 'Incorrect username or password.'}), 400

    return render_template("login.html")



@register_bp.route('/register', methods=['GET', 'POST'])
def register() -> Union[str, Tuple[str, int]]:
    """
    Render the registration page for `GET` requests and handle user registration for POST requests.

    Returns:
        - For `GET` requests, returns the rendered `HTML` template for the registration page.
        - For `POST` requests:
            - If registration is successful, returns a `JSON` response indicating success with a status code of `200`.
            - If an error occurs during registration, returns a `JSON` response indicating failure with a status code of `400`.

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
            password_confirm = data.get('password2')
            user_type = 'Trainer' if data.get('isTrainer') else 'Student'

            if password != password_confirm:
                return jsonify({'success': False, 'message': 'Passwords do not match!'}), 400

            response = cognito_service.register_user(email, password, user_type)

            # Check if the registration was successful
            if response.get('success'):
                # Call the S3Service.send_json_file method after successful registration
                S3Service.send_json_file(file_path='debug/test.json', object_key='user_data/filename.json')

                # Handle register response with a status code of 200
                return jsonify({'success': True, 'message': 'User registered successfully'}), 200
            else:
                # Handle registration failure with the response message and a status code of 400
                return jsonify({'success': False, 'message': response.get('message')}), 400

        except Exception as e:
            # Log the error
            log_error(str(e))
            print(str(e))

            # Split the error message using ': ' as the separator and take the second part
            error_message = str(e).split(': ', 2)[-1]

            # Handle registration failure with a specific error message and a status code of 400
            return jsonify({'success': False, 'message': error_message}), 400

    return render_template("register.html")
