from extensions import db


class User(db.Model):
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