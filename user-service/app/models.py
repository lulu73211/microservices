from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User:
    @staticmethod
    def create_user(data):
        data['password'] = generate_password_hash(data['password'])
        result = db.users.insert_one(data)
        return str(result.inserted_id)

    @staticmethod
    def find_by_email(email):
        return db.users.find_one({'email': email})

    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)
