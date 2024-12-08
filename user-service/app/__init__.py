from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)

    # Configuration de Flask
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Remplacez par une vraie clé secrète
    jwt = JWTManager(app)

    # Connexion à MongoDB
    client = MongoClient("mongodb://mongo:27017/")
    app.db = client.user_service

    # Enregistrer les routes
    from .routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/users')

    return app
