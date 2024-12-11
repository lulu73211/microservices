from flask import Flask, request, Response, jsonify
import requests
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt, get_jwt_identity

app = Flask(__name__)

# Configuration pour JWT
app.config['JWT_SECRET_KEY'] = 'm8c9tMJLa2KJcE5HjxkZ5kdYMx8xzERAPfT3wjvhKA8'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
jwt = JWTManager(app)

# Gestion des erreurs globales
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": "Une erreur a été recontrée, Veuillez patienter ou verifier la route que vous souhaitez accéder."}), 500


# Exemple : protéger une route avec JWT
@app.route('/payment', methods=['POST'])
@jwt_required()
def handle_payment():
    # Récupérer l'utilisateur actuel du token JWT
    user_id = get_jwt_identity()
    payload = { "userId": user_id, **request.json }
    try:
        subscription_response = requests.get('http://subscription-service:5002/api/subscriptions')
        
        if not subscription_response.ok:
            return Response(subscription_response.content, status=subscription_response.status_code, content_type=subscription_response.headers['Content-Type'])
        
        subscriptions = subscription_response.json() # Récupérer les abonnements []

        # Vérifier si l'utilisateur a un abonnement actif
        subscription_data = None
        for i in range(0, len(subscriptions)):
            if subscriptions[i]['userId'] == user_id and subscriptions[i]['_id'] == payload['subscriptionId']:
                subscription_data = subscriptions[i]
                break

        if subscription_data is None:
            return jsonify({"error": "Vous n'avez pas d'abonnement actif"}), 400

        response = requests.post('http://payment-service:5003/api/payments', json=payload)
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500

@app.route('/payment', methods=['PUT'])
@jwt_required()
def update_payments():
    # Récupérer l'utilisateur actuel du token JWT
    payment_id = request.args.get('id', None)
    try:
        response = requests.put(f"http://payment-service:5003/api/payments/{payment_id}", json=request.json)
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500

@app.route('/payment', methods=['GET'])
@jwt_required()
def get_payments():
       # Récupérer l'utilisateur actuel du token JWT
    user_id = get_jwt_identity()
    # Ajouter l'identifiant de l'utilisateur dans la requête
    payload = {"userId": user_id, **request.json}
    try:
        response = requests.get('http://payment-service:5003/api/payments', json=payload)
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500


@app.route('/subscription', methods=['POST'])
@jwt_required()
def handle_subscription():
    user_id = get_jwt_identity()
    user = {"userId": user_id, **request.json}
    try:
        response = requests.post(
            'http://subscription-service:5002/api/subscriptions',
            json=user
        )
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500

@app.route('/subscription', methods=['PUT'])
@jwt_required()
def update_subscription():
    subscription_id = request.args.get('id', None)
    try:
        response = requests.put(
            f"http://subscription-service:5002/api/subscriptions/{subscription_id}",
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
def register_user():
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
        response = requests.post('http://user-service:5001/api/users/login', json=request.json)

        if not response.ok:
            return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])

        user_id = response.json().get('user_id', None)
        access_token = create_access_token(identity=user_id)
        return jsonify(token_jwt=access_token), 200
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["POST"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)