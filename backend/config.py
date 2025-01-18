import os

class Config:
    # SQL secret key is required when using db.session
    SECRET_KEY = os.urandom(24)
    # PostgreSQL config template:"postgresql://<username>:<password>@localhost:<port_number>/<database_name>"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin123@localhost:5432/auth"
    # Set True in development to understand query behavior; False in production avoid performance impact and cluttering logs
    SQLALCHEMY_ECHO = False