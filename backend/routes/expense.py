from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from models.expense import Expense
from forms import ExpenseForm
from extensions import db, cache


expense_bp = Blueprint('expense', __name__, url_prefix='/expense')


@expense_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_expense():
    form = ExpenseForm()

    if form.validate_on_submit():
        # create a new expense record from form data
        new_expense = Expense(
            date=form.date.data,
            category=form.category.data,
            title=form.title.data,
            expense=form.expense.data,
            user_id=current_user.id
        )
        
        # add the new expense to the database
        db.session.add(new_expense)
        db.session.commit()

        # # trigger update db instead of wait cache timeout
        # cache.delete_memoized("home_cache")
        
        flash("Expense record created successfully!", "success")
        return redirect(url_for("home"))

    return render_template("create_expense_record.html", form=form)