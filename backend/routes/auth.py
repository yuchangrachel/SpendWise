from flask import Blueprint, render_template, redirect, url_for, flash, request,jsonify
from flask_login import login_required, login_user, logout_user
from app import bcrypt
from extensions import db
from models.users import User
from forms import RegisterForm
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, unset_jwt_cookies

# RabbitMQ configuration
EXCHANGE = 'activity_logs_exchange'
ROUTING_KEY = 'register'


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        if User.query.filter_by(email=email).first():
            flash("Email already exists", "danger")
        else:
            new_user = User(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("auth.login"))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", "danger")

    return render_template("register.html", form=form)

@auth_bp.route("/", methods=["GET"], endpoint="access_login")
def access_login():
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json 
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            access_token = create_access_token(identity=email)  # create JWT token

            response = jsonify({"message": "Login successful"})
            set_access_cookies(response, access_token)
            return response
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        # Catch any exceptions and return a 500 server error
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

    # form = LoginForm()
    # if form.validate_on_submit():
    #     email = form.email.data
    #     password = form.password.data
    #     user = User.query.filter_by(email=email).first()

    #     if user and bcrypt.check_password_hash(user.password, password):
    #         login_user(user)
    #         return redirect(url_for("home"))
    #     else:
    #         flash("Invalid email or password", "danger")
    # else:
    #     for field, errors in form.errors.items():
    #         for error in errors:
    #             flash(f"{field}: {error}", "danger")

    # return render_template("login.html", form=form)


# logout route
@auth_bp.route("/logout")
@login_required
def logout():
    # cache.delete("user_data_{}".format(current_user.id))
    logout_user()
    flash("Logged out successfully", "success")
    response = jsonify({"message": "Logout successfully"})
    response = redirect(url_for("auth.access_login"))  
    unset_jwt_cookies(response)
    return response

@auth_bp.route('/protected', methods=['GET'])
@login_required
@jwt_required()
def protected():
    return redirect(url_for("home"))
