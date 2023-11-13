from flask import Flask, render_template
from app.routes import home_bp, login_bp, register_bp

app = Flask(__name__, template_folder='app/templates')

# Register the blueprint
app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)

if __name__ == "__main__":
    app.run(debug=True)
