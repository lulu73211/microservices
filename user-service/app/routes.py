from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    if User.find_by_email(data['email']):
        return jsonify({'error': 'User already exists'}), 400

    user_id = User.create_user(data)
    return jsonify({'message': 'User created', 'user_id': user_id}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.find_by_email(data['email'])
    if not user or not User.verify_password(user['password'], data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = create_access_token(identity={'email': user['email']})
    return jsonify({'access_token': token}), 200

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    identity = get_jwt_identity()
    return jsonify({'profile': identity}), 200
