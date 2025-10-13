from cryptography.fernet import Fernet
from configs.cryptography import ENCRYPTION_KEY

fernet = Fernet(ENCRYPTION_KEY)

def encrypt_message( message : str) -> str:
    encrypted = fernet.encrypt(message.encode())
    return encrypted.decode()

def decrypt_message( message : str) -> str:
    decrypted = fernet.decrypt(message.encode())
    return decrypted.decode()


