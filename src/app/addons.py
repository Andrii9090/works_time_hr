from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.server import app

bcrypt = Bcrypt(app)
jwt = JWTManager(app)