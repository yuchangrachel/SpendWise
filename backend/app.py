"""
Backend main entry
"""
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from extensions import bcrypt, db, migrate
from routes.auth import auth_bp

 
app = Flask(__name__)

# load config from config.py
app.config.from_object("config.Config")
  
# call extensions and initialize app
bcrypt.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
CORS(app, supports_credentials=True)

  
# register Blueprints
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)