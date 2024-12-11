
# Microservices Project

## Description
Ce projet implémente une architecture basée sur des microservices, incluant les fonctionnalités suivantes :
- **User Service :** Gestion des utilisateurs (inscription et connexion).
- **Subscription Service :** Gestion des abonnements.
- **Payment Service :** Gestion des paiements.
- **API Gateway :** Point d'accès unique pour interagir avec les microservices.
- **RabbitMQ :** Communication asynchrone entre services.
- **MongoDB :** Base de données pour chaque service.

## Architecture
![Architecture Diagram](architecture_diagram.png) *(Ajoutez une image si possible)*

## Technologies utilisées
- **Node.js** : Pour les services `subscription-service` et `payment-service`.
- **Python (Flask)** : Pour `user-service` et `api-gateway`.
- **MongoDB** : Stockage des données pour chaque service.
- **RabbitMQ** : Messaging entre microservices.
- **Docker** : Conteneurisation et orchestration.

---

## Installation et déploiement

### Prérequis
- Docker et Docker Compose installés.

### Étapes pour lancer le projet
1. Clonez le dépôt :
   ```bash
   git clone <repository_url>
   cd microservices
   ```

2. Lancez tous les services avec Docker Compose :
   ```bash
   docker-compose up -d --build
   ```

3. Vérifiez que tous les conteneurs sont opérationnels :
   ```bash
   docker ps
   ```

---

## Utilisation

### 1. 📖 API Routes Documentation

Cette section décrit les différentes routes disponibles dans l'API Gateway, leur méthode HTTP, leurs paramètres, et les réponses attendues.

---

### **Authentication Routes**
#### **Login**
- **URL** : `http:localhost:5005/user/login`
- **Method** : `POST`
- **Description** : Authentifie un utilisateur et génère un token JWT.
- **Request Body** :
  | Parameter  | Type     | Description | Description       |
  | :--------- | :------- | :---------- | :---------------- |
  | `email`    | `string` | `required`  | the user email    |
  | `password` | `string` | `required`  | the user password |

- **Response** :
  - **200 OK** : Renvoie le token_jwt
  - **401 Unauthorized** : Informations d'identification invalides

---

### **Payment Routes**
#### **Create Payment**
- **URL** : `http:localhost:5005/payment`
- **Method** : `POST`
- **Description** : Crée un nouveau paiement (protection JWT requise).
- **Headers** :
  - `Authorization: Bearer <token_jwt>`
- **Request Body** :
  | Parameter        | Type     | Description | Description             |
  | :--------------- | :------- | :---------- | :---------------------- |
  | `subscriptionId` | `string` | `required`  | the subscription ID     |
  | `amount`         | `string` | `required`  | the payment amount      |
  | `paymentDate`    | `string` |             | the payment date        |

- **Response** :
  - **201 Created** : Détails du paiement créé.
  - **401 Unauthorized** : Si le JWT est manquant ou invalide.

#### **Get Payments**
- **URL** : `http:localhost:5005/payment`
- **Method** : `GET`
- **Description** : Récupère la liste des paiements (protection JWT requise).
- **Headers** :
  - `Authorization: Bearer <token_jwt>`
- **Response** :
  - **200 OK** : Liste des paiements.
  - **401 Unauthorized** : Si le JWT est manquant ou invalide.

---

### **Subscription Routes**
#### **Create Subscription**
- **URL** : `http:localhost:5005/subscription`
- **Method** : `POST`
- **Description** : Crée un nouvel abonnement (protection JWT requise).
- **Headers** :
  - `Authorization: Bearer <token_jwt>`
- **Request Body** :
  | Parameter     | Type     | Description | Description                   |
  | :------------ | :------- | :---------- | :---------------------------- |
  | `name`        | `string` | `required`  | the subscription name         |
  | `price`       | `string` | `required`  | the subscription price        |
  | `billingDate` | `string` |             | the subscription billing date |

- **Response** :
  - **201 Created** : Détails de l'abonnement créé.
  - **401 Unauthorized** : Si le JWT est manquant ou invalide.

#### **Get Subscriptions**
- **URL** : `http:localhost:5005/subscription`
- **Method** : `GET`
- **Description** : Récupère la liste des abonnements (protection JWT requise).
- **Headers** :
  - `Authorization: Bearer <token_jwt>`
- **Response** :
  - **200 OK** : Liste des abonnements.
  - **401 Unauthorized** : Si le JWT est manquant ou invalide.

---

### **User Management Routes**
#### **Register User**
- **URL** : `http:localhost:5005/user/register`
- **Method** : `POST`
- **Description** : Inscrit un nouvel utilisateur (protection JWT requise).
- **Headers** :
  - `Authorization: Bearer <token_jwt>`
- **Request Body** :
  | Parameter  | Type     | Description | Description       |
  | :--------- | :------- | :---------- | :---------------- |
  | `username` | `string` | `required`  | the username      |
  | `email`    | `string` | `required`  | the user email    |
  | `password` | `string` | `required`  | the user password |

- **Response** :
  - **201 Created** : Détails de l'utilisateur créé.
  - **401 Unauthorized** : Si le JWT est manquant ou invalide.


### Notes
- Toutes les routes protégées nécessitent un en-tête **Authorization** avec un token JWT valide :
  ```
  Authorization: Bearer <token_jwt>
  ```
- Utilisez un outil comme [Postman](https://www.postman.com/) ou `curl` pour tester les endpoints.

### 2. Commandes curl pour tester les endpoints
#### User Service
- **Inscription :**
  ```bash
  curl -X POST http://localhost:5005/user/register   -H "Content-Type: application/json"   -d '{"email": "user@example.com", "password": "password123"}'
  ```

- **Connexion :**
  ```bash
  curl -X POST http://localhost:5005/user/login   -H "Content-Type: application/json"   -d '{"email": "user@example.com", "password": "password123"}'
  ```

#### Subscription Service
- **Créer un abonnement :**
  ```bash
  curl -X POST http://localhost:5005/subscription   -H "Content-Type: application/json"   -d '{"userId": "12345", "name": "Netflix", "price": 12.99, "billingDate": "2024-12-15"}'
  ```

- **Lister les abonnements :**
  ```bash
  curl -X GET http://localhost:5005/subscription
  ```

#### Payment Service
- **Créer un paiement :**
  ```bash
  curl -X POST http://localhost:5005/payment   -H "Content-Type: application/json"   -d '{"userId": "12345", "subscriptionId": "abcde12345", "amount": 12.99, "paymentDate": "2024-12-15"}'
  ```

- **Lister les paiements :**
  ```bash
  curl -X GET http://localhost:5005/payment
  ```

---

## Dépannage
### Problèmes courants :
1. **Erreur de port déjà utilisé :**
   - Vérifiez quel processus utilise le port avec :
     ```bash
     sudo lsof -i :<port>
     ```
   - Tuez le processus :
     ```bash
     sudo kill -9 <PID>
     ```

2. **Service RabbitMQ indisponible :**
   - Vérifiez les logs du conteneur RabbitMQ :
     ```bash
     docker logs -f rabbitmq
     ```

3. **Logs d'un service spécifique :**
   ```bash
   docker logs -f <container_name>
   ```

---

## Améliorations futures
- Ajout de tests automatisés (unitaires et d'intégration).
- Implémentation d'une interface utilisateur (UI).
- Monitoring des services avec Prometheus et Grafana.
- Utilisation de différents langages pour les microservices.

---
