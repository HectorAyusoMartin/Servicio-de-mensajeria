"""
router con el endpoint para registrar usuarios.

"""

from fastapi import APIRouter, HTTPException, status
from app.models import UserCreate
from app.db import usuarios_collection
from app.utils.security import get_password_hash



router = APIRouter()

@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register_user(user : UserCreate):
    
    #!Verificamos primero si el usuario existe en la DB
    existing_user = await usuarios_collection.find_one({"username":user.username})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error, el usuario ya existe")
    
    
    #!Hasheamos la contraseña antes de guardarla
    hashed_password = get_password_hash(user.password)
    
    #!Guardamos el usuario con la pass hasheada
    user_data = {
        
        "username":user.username,
        "password":hashed_password 
        
    }
    
    result = await usuarios_collection.insert_one(user_data)
    if result.inserted_id:
        return {"msg":"Usuario registrado exitosamente"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error en el proceso de registro del usuario.")
    
    
if __name__ == "__main__":
        
    print('[O.K]')