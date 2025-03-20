"""
Modelo de datos para los mensajes del chat

"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class Message(BaseModel):
    
    username:str #!Usuario que envia el mensaje
    message:str #!Contenido del mensaje
    timestamp:datetime = datetime.utcnow() #! Esto hace un timestamp del tiempo actual
    
    model_config = ConfigDict(extra="forbid") #! Esto bloquea campos adicionales a los establecidos aqui.
    
    
    