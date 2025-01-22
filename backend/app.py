"""
Backend main entry
"""
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from extensions import bcrypt, db, migrate
from routes.auth import auth_bp
from routes.expense import expense_bp
from models.users import User
from datetime import timedelta
from models.expense import Expense 


app = Flask(__name__)


# load config from config.py
app.config.from_object("config.Config")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # session expires after 30 minutes


# initialize extensions
bcrypt.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"
CORS(app, supports_credentials=True)

# user loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(expense_bp)

# home route
@app.route("/")
@login_required
def home():
    # fetch expenses for the currently logged-in user
    expenses = Expense.query.filter_by(user_id=current_user.id).all()

    return render_template("home.html", expenses=expenses)


@app.errorhandler(404)
def page_not_found(e):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run(debug=True)
