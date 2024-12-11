from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from .models import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Vérifier si l'utilisateur existe déjà
    db = current_app.db
    if db.users.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    # Ajouter l'utilisateur
    user = User(email, password)
    db.users.insert_one({"email": user.email, "password": user.password})

    return jsonify({"message": "User registered successfully"}), 201

@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Rechercher l'utilisateur
    db = current_app.db
    user = db.users.find_one({"email": email})
    if not user or not User.check_password(user['password'], password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"user_id": str(user['_id'])}), 200
