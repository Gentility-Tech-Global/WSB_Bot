from cryptography.fernet import Fernet
import base64
import os

# Generate a key once and store it securely (env var, vault, etc.)
FERNET_SECRET = os.getenv("FERNET_SECRET_KEY") or Fernet.generate_key()
fernet = Fernet(FERNET_SECRET)

def encrypt_qr_data(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt_qr_data(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
