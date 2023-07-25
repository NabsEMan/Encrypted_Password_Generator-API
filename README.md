In the main file encrypted_password.py, we use the generate_password function to create a random password with options to include uppercase letters, digits, and special characters. We then use the generate_encrypted_password function to encrypt the generated password using the cryptography package and Fernet symmetric encryption. 
Finally, we can use the decrypt_password function to decrypt the encrypted password using the same encryption key.

We use the cryptography encryption library with secure key management. 
Please note that symmetric encryption requires the same key for both encryption and decryption. Keep the encryption key secure and do not share it with others. 
For decryption, you can use the same key with the Fernet object to reverse the encryption process and retrieve the original text.
