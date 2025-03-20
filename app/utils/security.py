"""
Funciones de hashing y autenticacion

"""

from passlib.context import CryptContext
from cryptography.fernet import Fernet
import os


#!Configuramos Bcrypt como algortimo de hashing
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

#📌Generar una clave AES única si no existe
KEY_PATH = "secret.key"

if not os.path.exists(KEY_PATH):
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)
else:
    with open(KEY_PATH, "rb") as key_file:
        key = key_file.read()

#📌Crear el objeto Fernet con la clave AES
cipher = Fernet(key)

def encrypt_message(message: str) -> str:
    """Cifra un mensaje usando AES y lo devuelve en base64."""
    encrypted_message = cipher.encrypt(message.encode())
    return encrypted_message.decode()

def decrypt_message(encrypted_message: str) -> str:
    """Descifra un mensaje cifrado con AES."""
    try:
        return cipher.decrypt(encrypted_message.encode()).decode()
    except Exception:
        return encrypted_message  # Si no está cifrado, lo devuelve tal cual.




def get_password_hash(password:str)->str:
    
    """Devuelve un hash de la contraseña proporcionada en formato string"""
    
    return pwd_context.hash(password)


def verify_password(plain_password:str,hashed_password:str)->bool:
    
    """Compara la clave en texto plano con su hash y devuelve True si la verificación es positiva."""
    
    return pwd_context.verify(plain_password,hashed_password)

