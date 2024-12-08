from flask import Flask, request, Response
import requests

app = Flask(__name__)

# Route pour gérer les paiements (POST)
@app.route('/payment', methods=['POST'])
def handle_payment():
    try:
        response = requests.post(
            'http://payment-service:5003/api/payments',
            json=request.json
        )
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500

# Route pour récupérer les paiements (GET)
@app.route('/payment', methods=['GET'])
def get_payments():
    try:
        response = requests.get('http://payment-service:5003/api/payments')
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500

# Route pour gérer les abonnements (POST)
@app.route('/subscription', methods=['POST'])
def handle_subscription():
    try:
        response = requests.post(
            'http://subscription-service:5002/api/subscriptions',
            json=request.json
        )
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500

# Route pour récupérer les abonnements (GET)
@app.route('/subscription', methods=['GET'])
def get_subscriptions():
    try:
        response = requests.get('http://subscription-service:5002/api/subscriptions')
        return Response(response.content, status=response.status_code, content_type=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500

# Route pour gérer les utilisateurs (POST - inscription)
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

# Route pour gérer les utilisateurs (POST - connexion)
@app.route('/user/login', methods=['POST'])
def login_user():
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

