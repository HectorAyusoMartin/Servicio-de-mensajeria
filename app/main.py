"""
Punto de entrada a la aplicación

"""


"""

3. Implementación Inicial
3.1. Backend Básico con Autenticación y WebSockets
A continuación te muestro un ejemplo en el archivo main.py que integra autenticación con JWT y un endpoint de WebSocket para el chat:


"""

from fastapi import FastAPI
from app.routers.users import router as users_router
from app.routers.chat import router as chat_router



app = FastAPI()


#!Incluimos el endpoint del usuarios
app.include_router(users_router)
app.include_router(chat_router)



