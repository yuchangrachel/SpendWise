"""
Flask-WTF: The UserForm handles the form rendering, validation, and submission
Use for form.validate_on_submit()
Frontend submits data as application/x-www-form-urlencoded
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, FloatField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Invalid email format."),
            Length(max=100)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required.")
        ]
    )
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Invalid email format."),
            Length(max=100)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required."),
            Length(min=3, message="Password must be at least 3 characters.")
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message="Password confirmation is required."),
            EqualTo('password', message="Passwords must match.")
        ]
    )
    submit = SubmitField('Register')


class ExpenseForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Entertainment', 'Entertainment'),
        ('Utilities', 'Utilities'),
        ('Health', 'Health')
    ], validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=100)])
    expense = FloatField('Expense ($)', validators=[DataRequired(), NumberRange(min=0)])

    submit = SubmitField('Create Expense Record')