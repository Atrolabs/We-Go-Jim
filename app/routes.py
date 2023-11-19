from flask import Blueprint, render_template, request, jsonify

home_bp = Blueprint("home", __name__)
login_bp = Blueprint("login", __name__)
register_bp = Blueprint("register", __name__)
submit_bp = Blueprint("submit", __name__)

@home_bp.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html")

@submit_bp.route('/submit', methods=['POST'])
def submit():
    data = {}

    # Get the JSON data from the request
    json_data = request.json

    data['role'] = 'Trainer' if json_data.get('isTrainer') else 'Student'

    #print(data)
    print(json_data)

    return 'Form submitted successfully!'