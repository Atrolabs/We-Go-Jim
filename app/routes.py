from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for

from services.cognito_service import CognitoService
from services.s3_service import S3Service

from typing import Union, Tuple

from utils.cognito_utils import decode_cognito_jwt, login_required
from utils.logs_utils import configure_logging, log_error
from models.models import UserExerciseModel, TrainerModel, RecordsModel

import plotly.graph_objs as go

configure_logging()

# Define Flask Blueprints for different parts of the applications
login_bp = Blueprint("login", __name__)
register_bp = Blueprint("register", __name__)
dashboard_bp = Blueprint("dashboard", __name__)
add_workout_bp = Blueprint("add-workout", __name__)
my_workouts_bp = Blueprint("my-workouts", __name__)
logout_bp = Blueprint("logout", __name__)
my_students_bp = Blueprint("my-students", __name__)
my_records_bp = Blueprint("my-records", __name__)

# Create an instance of CognitoService to interact with Amazon Cognito
cognito_service = CognitoService()  
s3_service = S3Service()


@dashboard_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    """Render the dashboard page"""
    # Retrieve user_sub from the session
    user_sub = session.get('user_sub') 
    email = session.get('email')
    user_type= session.get('user_type')
    return render_template('dashboard.html', user_sub=user_sub, email=email, user_type=user_type)



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
    if 'user_sub' in session:
        # User is already logged in, redirect to the dashboard
        return redirect(url_for('dashboard.dashboard'))
    
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
                user_type = cognito_service.get_user_attrib_by_sub(user_sub, 'custom:user_type')


                # Set up user session
                session['user_sub'] = user_sub
                session['user_type'] = user_type
                session['email'] = email

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

    if 'user_sub' in session:
        # User is already logged in, redirect to the dashboard
        return redirect(url_for('dashboard.dashboard'))
    
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

            user_sub = response['UserSub']
            s3_service.s3_init_user(user_sub=user_sub)
            s3_service.s3_init_user_records(user_sub=user_sub)
            # Handle register response with a status code of 200
            return jsonify({'success': True, 'message': 'User registered successfully'}), 200
        except Exception as e:
            # Log the error
            log_error(str(e))

            # Split the error message using ': ' as the separator and take the second part
            error_message = str(e).split(': ', 2)[-1]
            
            # Handle registration failure with a specific error message and a status code of 400
            return jsonify({'success': False, 'message': error_message}), 400

    return render_template("register.html")



@add_workout_bp.route('/add-workout', methods=['GET', 'POST'])
@login_required
def add_workout():
    try:
        user_type = session.get('user_type')

        if user_type != "Trainer":
            # If the user is not a Trainer, render a template with the message
            return render_template('not_allowed.html')

        if request.method == 'GET':
            # Handle the GET request to display the add_workout.html page for Trainers
            return render_template('add_workout.html', user_type=user_type)

        elif request.method == 'POST':
            email = request.json.get('email')
            user_sub = cognito_service.get_sub_by_email(email)

            # Check if the user exists in Cognito
            if user_sub is None or not cognito_service.check_user_exists(user_sub):
                return jsonify({"success": False, "message": "User not found"}), 404

            workout_plan = request.json.get('workout_plan', [])
            trainer_sub = session.get('user_sub')

            students_list = s3_service.get_student_list(trainer_sub)

            if not students_list:
                students_list = []

            if email not in students_list:
                students_list.append(email)

            trainer_model = TrainerModel(user_sub=trainer_sub, students=students_list)
            
            s3_service.add_student_to_list(trainer_model=trainer_model)

            user_exercise_model = UserExerciseModel(user_sub=user_sub, current_trainer=trainer_sub, workout_plan=workout_plan)

            if s3_service.s3_update_user_exercise(user_sub, user_exercise_model):
                return jsonify({"success": True, "message": "Workout added successfully"}), 200
            else:
                return jsonify({"success": False, "message": "Failed to add workout"}), 500

    except Exception as e:
        log_error(str(e))
        return jsonify({'success': False, 'message': 'An error occurred while adding the workout.'}), 500
    

@my_workouts_bp.route('/my-workouts', methods=['GET'])
@login_required
def my_workouts():
    try:
        # Retrieve user_sub from the request headers or session, depending on your authentication mechanism
        user_sub = session.get('user_sub') 
        email = cognito_service.get_user_attrib_by_sub(user_sub, 'email')
        if user_sub:
            # Retrieve user data from S3
            user_data = s3_service.s3_get_user_data(user_sub)
            trainer_sub = user_data.get('current_trainer', None)
            trainer_email = cognito_service.get_user_attrib_by_sub(trainer_sub, 'email')

            if user_data:
                user_type = session.get('user_type')
                # return jsonify(user_data)
                return render_template('my_workouts.html', user_data=user_data, user_type=user_type, trainer_email=trainer_email)
            else:
                return jsonify({'error': 'User data not found'}), 404
        else:
            return jsonify({'error': 'User not authenticated'}), 401
    except Exception as e:
        log_error(str(e))
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    


@logout_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login.login'))


@my_students_bp.route('/my-students', methods=['GET'])
@login_required
def display_my_students():
    try:
        user_type = session.get('user_type')
        if user_type != "Trainer":
            # If the user is not a Trainer, render a template with the message
            return render_template('not_allowed.html')
        # Get the trainer_sub from the current user's session or any other means
        trainer_sub = session.get('user_sub')

        # Assuming you have an instance of YourClass called 'your_instance'
        student_list = s3_service.get_student_list(trainer_sub)
        if not student_list:
            student_list = []

        # Create a dictionary to store the charts for each student
        student_charts = []

        # Loop through each student and create a chart for each one
        for student in student_list:
            # Fetch the current records from S3 for the student
            student_sub = cognito_service.get_sub_by_email(student)
            user_records = s3_service.get_user_records(student_sub)
            print(student_sub)
            print(user_records)

            # Create a Plotly line chart
            chart = go.Figure()

            # Loop through each exercise and add a separate line to the chart for each exercise
            for exercise in user_records:
                exercise_name = exercise['name']
                weights = exercise['weight']
                chart.add_trace(go.Scatter(x=list(range(len(weights))), y=weights, mode='lines+markers', name=exercise_name))

            # Convert the chart to HTML
            chart_html = chart.to_html(full_html=False)

            # Add the chart to the dictionary
            student_charts.append(chart_html)

        # Render the student list and charts in an HTML template
        email = session.get('email')
        return render_template('my_students.html', student_list=student_list, trainer_sub=trainer_sub, user_type=user_type, email=email, student_charts=student_charts)

    except Exception as e:
        log_error(str(e))
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    

@my_records_bp.route('/my-records', methods=['GET', 'POST'])
@login_required
def my_records():
    try:
        if request.method == 'GET':
            # Display the form
            email = session.get('email')
            user_sub = session.get('user_sub')
            user_type = session.get('user_type')

            # Fetch the current records from S3
            user_records = s3_service.get_user_records(user_sub)
            
            # Create a Plotly line chart
            chart = go.Figure()

            # Loop through each exercise and add a separate line to the chart for each exercise
            for exercise in user_records:
                exercise_name = exercise['name']
                weights = exercise['weight']
                chart.add_trace(go.Scatter(x=list(range(len(weights))), y=weights, mode='lines+markers', name=exercise_name))

            # Convert the chart to HTML
            chart_html = chart.to_html(full_html=False)

            return render_template('my_records.html', user_sub=user_sub, email=email, user_type=user_type, user_records=user_records, chart_html=chart_html)

        elif request.method == 'POST':
            # Process form submission
            user_sub = session.get('user_sub')
            data = request.get_json()
            exercise_name = data['exercise_name']
            new_record = float(data['new_record'])

            # Fetch the current records from S3
            user_records = s3_service.get_user_records(user_sub)

            # Update the specific exercise record
            for exercise in user_records:
                if exercise['name'] == exercise_name:
                    exercise['weight'].append(new_record)
                    break

            # Create a UserModel instance with updated data
            updated_user_model = RecordsModel(user_sub=user_sub, records_list=user_records)

            # Update the records in S3
            success = s3_service.update_user_records(updated_user_model)

            if success:
                return "Records updated successfully"
            else:
                return "Error updating records"

    except Exception as e:
        log_error(str(e))
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    