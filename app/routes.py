from flask import Blueprint, render_template, request, jsonify
from services.cognito_service import CognitoService  # Import the CognitoService

home_bp = Blueprint("home", __name__)
login_bp = Blueprint("login", __name__)
register_bp = Blueprint("register", __name__)

cognito_service = CognitoService()  # Create an instance of CognitoService

@home_bp.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            data = request.json  # Use request.json to handle JSON data
            email = data.get('email')
            password = data.get('password1')
            user_type = 'Trainer' if data.get('isTrainer') else 'Student'

            response = cognito_service.register_user(email, password, user_type)

            # Note: For debugging purposes only. Remove the following line in production.
            print(response)

            return jsonify({'success': True, 'message': 'User registered successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    return render_template("register.html") 
