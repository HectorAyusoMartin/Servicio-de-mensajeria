"""
Modelo de datos para los mensajes del chat

"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class Message(BaseModel):
    
    username:str
    message:str
    timestamp:datetime = datetime.utcnow() #! Esto hace un timestamp del tiempo actual
    
    model_config = ConfigDict(extra="forbid") #! Esto bloquea campos adicionales a los establecidos aqui.
    
    
    