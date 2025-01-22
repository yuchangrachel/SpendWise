"""
Backend main entry
"""
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, current_user
from flask_cors import CORS
from extensions import bcrypt, db, migrate
from routes.auth import auth_bp
from routes.expense import expense_bp
from models.users import User
from models.expense import Expense 


app = Flask(__name__)


# load config from config.py
app.config.from_object("config.Config")

# initialize extensions & configs
# cache.init_app(app)
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
# @cache.cached(timeout=60, key_prefix="user_data_{}.format(current_user.id)")
def home():
    # get sort order from query string, default sort Date
    sort_by = request.args.get('sort_by', 'date')
    sort_order = request.args.get('sort_order', 'asc')

    # fetch expense for currently logged-in user
    expenses = Expense.query.filter_by(user_id=current_user.id)

    # apply sorting dynamically
    if hasattr(Expense, sort_by): 
        if sort_order == 'asc':
            expenses = expenses.order_by(getattr(Expense, sort_by).asc())
        else:
            expenses = expenses.order_by(getattr(Expense, sort_by).desc())

    # get page number(default 1) from query string
    page = request.args.get('page', 1, type=int)
    # set number of expenses per page
    per_page = 3 
    # fetch expenses for the currently logged-in user
    expenses = expenses.paginate(page=page, per_page=per_page, error_out=False)

    return render_template("home.html", expenses=expenses, sort_by=sort_by, sort_order=sort_order)

# handle unexpected routes
@app.errorhandler(404)
def page_not_found(e):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("auth.login"))


if __name__ == "__main__":
    app.run(debug=True)
