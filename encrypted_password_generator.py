from flask import Flask, request, jsonify
from flasgger import Swagger
import random
import string
from cryptography.fernet import Fernet
from flasgger import Swagger, swag_from

app = Flask(__name__)
Swagger(app)

# Function that returns a random password, of 8 character long at least,  with options for upper case, numbers, and special characters
def generate_password(length=12, uppercase=True, digits=True, special_chars=True):
    password_characters = string.ascii_lowercase
    if uppercase:
        password_characters += string.ascii_uppercase
    if digits:
        password_characters += string.digits
    if special_chars:
        password_characters += string.punctuation

    secure_password = ''.join(random.choice(password_characters) for _ in range(length))
    return secure_password

# Function that returns an encrypted random password, of 8 character long at least,  with options for upper case, numbers, and special characters, the encrypted password and the encryption key
def generate_encrypted_password(length=12, uppercase=True, digits=True, special_chars=True, encryption_key=None):
    password = generate_password(length, uppercase, digits, special_chars)
    if encryption_key is None:
        encryption_key = Fernet.generate_key()

    fernet = Fernet(encryption_key)
    encrypted_password = fernet.encrypt(password.encode('utf-8'))
    return password, encrypted_password, encryption_key

# Function that returns the decrypted poassword from encrypted versiona and its encryption key
def decrypt_password(encrypted_password, encryption_key):
    fernet = Fernet(encryption_key)
    decrypted_password = fernet.decrypt(encrypted_password).decode('utf-8')
    return decrypted_password

@app.route('/generate_password', methods=['GET'])
def generate_encrypted_password_api():
    """
    Generate an encrypted password
    ---
    parameters:
      - name: length
        in: query
        type: integer
        required: false
        default: 12
      - name: uppercase
        in: query
        type: boolean
        required: false
        default: true
      - name: digits
        in: query
        type: boolean
        required: false
        default: true
      - name: special_chars
        in: query
        type: boolean
        required: false
        default: true
    responses:
      200:
        description: Password generated and encrypted successfully.
        schema:
          type: object
          properties:
            password:
              type: string
            encrypted_password:
              type: string
            encryption_key:
              type: string
      400:
        description: Invalid input. Check the request parameters.
    """
    length = int(request.args.get('length', 12))
    uppercase = bool(request.args.get('uppercase', True))
    digits = bool(request.args.get('digits', True))
    special_chars = bool(request.args.get('special_chars', True))

    password, encrypted_password, encryption_key = generate_encrypted_password(length, uppercase, digits, special_chars)
    return jsonify({"password": password, "encrypted_password": encrypted_password, "encryption_key": encryption_key.decode('utf-8')}), 200@app.route('/')

@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to our Encrypted_Password_Generator-API!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)

