
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

### 1. Tester les endpoints avec Postman
Importez la collection Postman fournie dans le projet (fichier `.json`).

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
