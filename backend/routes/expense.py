import os
import random
import string
from flask import render_template, redirect, url_for, flash, Blueprint, request, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.expense import Expense
from forms import ExpenseForm
from extensions import db
from datetime import datetime


expense_bp = Blueprint('expense', __name__, url_prefix='/expense')

UPLOAD_EXPENSE = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_EXPENSE):
    os.makedirs(UPLOAD_EXPENSE)


def valiate_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

        # handle file upload
        receipt = request.files.get('receipt')
        if receipt and valiate_file(receipt.filename):
            filename = secure_filename(receipt.filename)

            # make filename unique 
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            new_filename = f"{timestamp}_{random_str}_{filename}"

            # save file in disk
            file_path = os.path.join(UPLOAD_EXPENSE, new_filename)
            receipt.save(file_path)

            # store the file path in the database
            new_expense.receipt_path = file_path

        # add the new expense to the database
        db.session.add(new_expense)
        db.session.commit()
        
        flash("Expense record created successfully!", "success")
        return jsonify({'success': True, 'message': 'Expense record created successfully!'})

    return render_template("create_expense_record.html", form=form)


@expense_bp.route("/receipt/<int:expense_id>")
@login_required
def view_receipt(expense_id):
    expense = Expense.get_expense(expense_id=expense_id, user_id=current_user.id)

    if not expense or not expense.receipt_path:
        flash("Receipt not found or access denied!", "danger")
        return redirect(url_for("home"))
    
    # store db is relative path start with static/, urls for must have static/ as prefix, remove dup
    if expense.receipt_path.startswith("static/"):
        receipt_relative_path = expense.receipt_path[len("static/"):]
    else:
        receipt_relative_path = expense.receipt_path

    # serve the receipt URL dynamically
    receipt_url = url_for('static', filename=receipt_relative_path)
    return {"receipt_url": receipt_url}, 200