from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from models.expense import Expense
from forms import ExpenseForm
from extensions import db


expense_bp = Blueprint('expense', __name__, url_prefix='/expense')

# Home route
@expense_bp.route("/", methods=["GET"])
@login_required
def home():
    # Query the Expense model for the current user's expenses
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    
    # Render home.html with the fetched expenses
    return render_template("home.html", expenses=expenses)


@expense_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_expense():
    form = ExpenseForm()

    if form.validate_on_submit():
        # Create a new expense record from form data
        new_expense = Expense(
            date=form.date.data,
            category=form.category.data,
            title=form.title.data,
            expense=form.expense.data,
            user_id=current_user.id
        )
        
        # Add the new expense to the database
        db.session.add(new_expense)
        db.session.commit()
        
        flash("Expense record created successfully!", "success")
        return redirect(url_for("expense.home"))

    return render_template("create_expense_record.html", form=form)