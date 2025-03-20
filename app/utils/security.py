"""
Funciones de hashing y autenticacion

"""

from passlib.context import CryptContext


#!Configuramos Bcrypt como algortimo de hashing
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")




def get_password_hash(password:str)->str:
    
    """Devuelve un hash de la contraseña proporcionada en formato string"""
    
    return pwd_context.hash(password)


def verify_password(plain_password:str,hashed_password:str)->bool:
    
    """Compara la clave en texto plano con su hash y devuelve True si la verificación es positiva."""
    
    return pwd_context.verify(plain_password,hashed_password)

