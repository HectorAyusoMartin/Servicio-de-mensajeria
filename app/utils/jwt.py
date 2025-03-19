from datetime import timedelta , datetime
from jose import JWTError, jwt
import os
from dotenv import load_dotenv


#!Cargamos las variables de entorno
load_dotenv()


#!Configuramos JWT
SECRET_KEY = os.getenv("JWT_SECRET","secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


def create_access_token(data:dict,expires_delta: timedelta | None = None):
    """ Genera un token JWT con los datos proporcionados y una expriacion"""
    
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    


def verify_access_token(token:str):
    """ Verifica un token JWT y retorna sus datos si este es valido,."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    
    except JWTError:
        return None



