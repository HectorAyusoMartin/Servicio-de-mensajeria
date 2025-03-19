"""
Punto de entrada a la aplicación

"""


"""

3. Implementación Inicial
3.1. Backend Básico con Autenticación y WebSockets
A continuación te muestro un ejemplo en el archivo main.py que integra autenticación con JWT y un endpoint de WebSocket para el chat:


"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
import motor.motor_asyncio


app = FastAPI()

# Variables de seguridad
SECRET_KEY = "CLAVE_SUPER_SECRETA"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30


# Configuracion a la base de datos
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.chat_app

# Contexto para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

