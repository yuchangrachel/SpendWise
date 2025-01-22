import os
from datetime import timedelta

class Config:
    # SQL secret key is required when using db.session
    SECRET_KEY = os.urandom(24)
    # PostgreSQL config template:"postgresql://<username>:<password>@localhost:<port_number>/<database_name>"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin123@localhost:5432/auth"
    # Set True in development to understand query behavior; False in production avoid performance impact and cluttering logs
    SQLALCHEMY_ECHO = False
    # CACHE_TYPE = 'simple' for development; 'redis' for production
    CACHE_TYPE = 'SimpleCache'
    # Session expires after 30 minutes
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

