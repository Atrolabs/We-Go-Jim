from flask import Flask
from config.config_loader import FLASK_SECRET_KEY

def create_app():
    app = Flask(__name__)

    # Set Flask secret key
    app.config['SECRET_KEY'] = FLASK_SECRET_KEY

    # Register blueprints, configure app, etc.
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    from app.routes import login_bp, register_bp, dashboard_bp, add_workout_bp, my_workouts_bp, logout_bp, my_students_bp, my_records_bp
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(add_workout_bp)
    app.register_blueprint(my_workouts_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(my_students_bp)
    app.register_blueprint(my_records_bp)


    return app
