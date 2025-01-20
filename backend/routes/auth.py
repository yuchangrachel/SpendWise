from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from app import bcrypt
from extensions import db
from models.users import User
 
auth_bp = Blueprint("auth", __name__)

# Flask use function name as endpoint name
@auth_bp.route("/home", methods=["GET"], endpoint="home")
@login_required
def dashboard():
    return render_template("home.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        if User.query.filter_by(email=email).first():
            flash("Email already exists", "danger")
        else:
            new_user = User(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("auth.home"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")


# Logout route
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))