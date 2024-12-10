from flask import Flask, request, Response, jsonify
import requests
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)

# Configuration pour JWT
app.config['JWT_SECRET_KEY'] = 'm8c9tMJLa2KJcE5HjxkZ5kdYMx8xzERAPfT3wjvhKA8'
jwt = JWTManager(app)

# Gestion des erreurs globales
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": "Une erreur a été recontrée, Veuillez patienter ou verifier la route que vous souhaitez accéder."}), 500


# Route pour générer un token JWT (Login)
@app.route('/user/login', methods=['POST'])
def login_user():
    try:
        # Simuler un utilisateur valide pour cet exemple
        if request.json.get("username") == "admin" and request.json.get("password") == "password":
            # Créer un token JWT
            access_token = create_access_token(identity={"username": "admin"})
            return jsonify(access_token=access_token), 200
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return {"error": str(e)}, 500


# Exemple : protéger une route avec JWT
@app.route('/payment', methods=['POST'])
@jwt_required()
def handle_payment():
    current_user = get_jwt_identity()  # Récupérer l'utilisateur actuel du token JWT
    try:
        response = requests.post(
            'http://payment-service:5003/api/payments',
            json=request.json
        )
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500


@app.route('/payment', methods=['GET'])
@jwt_required()
def get_payments():
    current_user = get_jwt_identity()  # Récupérer l'utilisateur actuel
    try:
        response = requests.get('http://payment-service:5003/api/payments')
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500


@app.route('/subscription', methods=['POST'])
@jwt_required()
def handle_subscription():
    current_user = get_jwt_identity()
    try:
        response = requests.post(
            'http://subscription-service:5002/api/subscriptions',
            json=request.json
        )
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500


@app.route('/subscription', methods=['GET'])
@jwt_required()
def get_subscriptions():
    current_user = get_jwt_identity()
    try:
        response = requests.get('http://subscription-service:5002/api/subscriptions')
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500


@app.route('/user/register', methods=['POST'])
@jwt_required()
def register_user():
    current_user = get_jwt_identity()
    try:
        response = requests.post(
            'http://user-service:5001/api/users/register',
            json=request.json
        )
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500


@app.route('/user/login', methods=['POST'])
def user_login():
    try:
        response = requests.post(
            'http://user-service:5001/api/users/login',
            json=request.json
        )
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)