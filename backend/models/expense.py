from extensions import db

class Expense(db.Model):
    """
    Expense model for storing user expenses.

    Columns:
        id (int): Primary key.
        date (date): The date of the expense.
        category (str): Expense category.
        title (str): A brief title or description of the expense.
        expense (float): The amount spent.
        receipt_path(str): relative path of image
    """
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    expense = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receipt_path = db.Column(db.String(200), nullable=True)

    user = db.relationship('User', backref='expenses', lazy=True)

    def __repr__(self):
        return f"<Expense {self.title} - ${self.expense}>"
    
    @classmethod
    def get_expense(cls, expense_id, user_id):
        return cls.query.filter_by(id=expense_id, user_id=user_id).first()