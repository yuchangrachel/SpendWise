"""
Backend main entry
"""
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from models import db
from routes.auth import auth_bp

 
app = Flask(__name__)

# load config from config.py
app.config.from_object("config.Config")
  
bcrypt = Bcrypt(app) 
CORS(app, supports_credentials=True)
db.init_app(app)
migrate = Migrate(app, db)
  
# register Blueprints
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)