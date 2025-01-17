from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/your_database'
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        from .routes import auth
        app.register_blueprint(auth)

        db.create_all()

    return app
