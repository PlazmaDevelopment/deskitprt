import os
import tempfile
import pytest
from deskitprt.crypto import generate_key, encrypt_file, decrypt_file

def test_generate_key():
    key1, salt1 = generate_key("test_password")
    key2, salt2 = generate_key("test_password", salt1)
    
    assert len(key1) > 0
    assert len(salt1) == 16
    assert key1 == key2
    assert salt1 == salt2

def test_encrypt_decrypt_file():
    # Create a test file
    with tempfile.NamedTemporaryFile(delete=False) as f:
        test_file = f.name
        f.write(b"Test content")
    
    try:
        # Test encryption
        encrypted_file = encrypt_file(test_file, "test_password")
        assert os.path.exists(encrypted_file)
        
        # Test decryption
        decrypted_file = decrypt_file(encrypted_file, "test_password")
        assert decrypted_file == test_file
        
        # Verify content
        with open(decrypted_file, 'rb') as f:
            content = f.read()
        assert content == b"Test content"
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        if 'encrypted_file' in locals() and os.path.exists(encrypted_file):
            os.remove(encrypted_file)

def test_wrong_password():
    # Create a test file
    with tempfile.NamedTemporaryFile(delete=False) as f:
        test_file = f.name
        f.write(b"Test content")
    
    try:
        # Encrypt with one password
        encrypted_file = encrypt_file(test_file, "password1")
        
        # Try to decrypt with wrong password
        result = decrypt_file(encrypted_file, "wrong_password")
        assert result is None
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        if 'encrypted_file' in locals() and os.path.exists(encrypted_file):
            os.remove(encrypted_file)
