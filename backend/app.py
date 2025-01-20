"""
Backend main entry
"""
from flask import Flask, render_template
from flask_login import LoginManager, login_required
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from extensions import bcrypt, db, migrate
from routes.auth import auth_bp
from models.users import User

app = Flask(__name__)

# load config from config.py
app.config.from_object("config.Config")

# initialize extensions
bcrypt.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"
CORS(app, supports_credentials=True)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# register blueprints
app.register_blueprint(auth_bp)

# Home route
@app.route("/")
@login_required
def home():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
