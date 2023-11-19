from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register blueprints, configure app, etc.
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    from app.routes import home_bp, login_bp, register_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)

    return app
