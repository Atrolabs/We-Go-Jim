from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)
login_bp = Blueprint("login", __name__)
register_bp = Blueprint("register", __name__)

@home_bp.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html")