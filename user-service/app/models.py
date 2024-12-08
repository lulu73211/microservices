from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    @staticmethod
    def check_password(hashed_password, plain_password):
        return check_password_hash(hashed_password, plain_password)
