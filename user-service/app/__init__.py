from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from config import Config

db = None

def create_app():
    global db
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize MongoDB
    client = MongoClient(app.config['MONGO_URI'])
    db = client.get_default_database()

    # Initialize JWT
    JWTManager(app)

    from app.routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/users')

    return app
