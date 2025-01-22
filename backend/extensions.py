"""
Initialize extensions once
"""
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache

bcrypt = Bcrypt() 
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()