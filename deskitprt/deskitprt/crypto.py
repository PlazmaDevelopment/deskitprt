import os
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def generate_key(password: str, salt: bytes = None):
    """Generate encryption key from password"""
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def encrypt_file(file_path: str, password: str):
    """Encrypt a file with the given password"""
    salt = os.urandom(16)
    key, salt = generate_key(password, salt)
    fernet = Fernet(key)
    
    with open(file_path, 'rb') as file:
        file_data = file.read()
    
    encrypted_data = fernet.encrypt(file_data)
    
    encrypted_file_path = f"{file_path}.encrypted"
    with open(encrypted_file_path, 'wb') as file:
        file.write(salt + encrypted_data)
    
    os.remove(file_path)
    return encrypted_file_path

def decrypt_file(encrypted_file_path: str, password: str):
    """Decrypt a file with the given password"""
    with open(encrypted_file_path, 'rb') as file:
        file_data = file.read()
    
    salt = file_data[:16]
    encrypted_data = file_data[16:]
    
    key, _ = generate_key(password, salt)
    fernet = Fernet(key)
    
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        original_file_path = encrypted_file_path.replace('.encrypted', '')
        
        with open(original_file_path, 'wb') as file:
            file.write(decrypted_data)
        
        os.remove(encrypted_file_path)
        return original_file_path
    except Exception as e:
        print(f"Error decrypting file: {e}")
        return None
