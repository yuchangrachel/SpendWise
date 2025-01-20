from extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """
    User model
    
    Columns:
        id (int): User ID
        email (str): User email
        password (str): User password
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    is_active_user = db.Column(db.Boolean, default=True)

    @property
    def is_active(self):
        return self.is_active_user