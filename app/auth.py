from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

# Define users that will hold all users and their hashed passwords
users = {"user": generate_password_hash("password")}

@auth.verify_password
def verify_password(username, password):
    # Check if username exists and matches the password
    if username in users and check_password_hash(users.get(username), password):
        return username
