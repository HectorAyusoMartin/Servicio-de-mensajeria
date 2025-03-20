"""
Modelo de datos para Usuarios

"""

from pydantic import BaseModel, Field, ConfigDict

class UserCreate(BaseModel):
    
    """
    estructura de los datos que recibiremos al registrar un usuario
    
    UserCreate es un modelo que valida que el nombre de usuario tenga entre 3 y 50 caracteres y que la contraseña tenga al menos 6 caracteres.
    Esto nos ayuda a asegurarnos de que los datos recibidos sean correctos antes de procesarlos.
    
    """
    
    username:str = Field(..., min_length=3, max_length=50)
    password:str = Field(..., min_length=6)
    
    
    model_config = ConfigDict(extra="forbid") #! Esto bloquea campos adicionales a los establecidos aqui.
    
    
    