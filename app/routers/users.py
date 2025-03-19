"""
router con el endpoint para registrar usuarios.

"""

from fastapi import APIRouter, HTTPException, status
from app.models import User_create
from app.db import usuarios_collection


router = APIRouter()

@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register_user(user : User_create):
    
    #!Verificamos primero si el usuario existe en la DB
    existing_user = await usuarios_collection.find_one({"username":user.username})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error, el usuario ya existe")
    
    #!Guardamos el usuario( sin hasehar la pass todavia, se hara en el futuro)
    user_data = {
        "username":user.username,
        "password":user.password #!-> Por ahora como digo, sin hashear
    }
    
    result = await usuarios_collection.insert_one(user_data)
    if result.inserted_id:
        return {"msg":"Usuario registrado exitosamente"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error en el proceso de registro del usuario.")