from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Dictionnaire pour mapper les services
SERVICES = {
    "user": "http://user-service:5001/api/users",
    "subscription": "http://subscription-service:5002/api/subscriptions",
    "payment": "http://payment-service:5003/api/payments"
}

@app.route('/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(service, path):
    # Vérifiez si le service demandé existe
    if service not in SERVICES:
        return jsonify({"error": f"Service '{service}' not found"}), 404

    # Construisez l'URL de redirection
    url = f"{SERVICES[service]}/{path}"
    
    # Redirigez la requête au service correspondant
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers if key != 'Host'},
            json=request.get_json(),
            params=request.args
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
