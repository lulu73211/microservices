import unittest
from app import create_app
from flask import json

class UserServiceAPITest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()  # Assurez-vous que create_app() existe dans app.py
        self.client = self.app.test_client()

    def test_register_user(self):
        payload = {
            "email": "test@test.com",
            "password": "password123"
        }
        response = self.client.post('/api/users/register', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn('email', response.json)

    def test_login_user(self):
        # Inscrire un utilisateur pour le connecter ensuite
        self.client.post('/api/users/register', json={"email": "test@test.com", "password": "password123"})
        
        payload = {
            "email": "test@test.com",
            "password": "password123"
        }
        response = self.client.post('/api/users/login', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

if __name__ == "__main__":
    unittest.main()
