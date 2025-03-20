"""
router con el endpoint para registrar usuarios.

"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.users import UserCreate
from app.db import usuarios_collection
from app.utils.security import get_password_hash, verify_password
from app.utils.jwt import create_access_token
from datetime import timedelta





router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


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
    
@router.post("/login")
async def login(form_data : OAuth2PasswordRequestForm = Depends()):
    
    """
    Autentica al usuario y devuelve un token JWT si las credenciales son correctas
    
    """
    
    user = await usuarios_collection.find_one({"username":form_data.username})
    
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="La contraseña no es correcta")
    
    access_token = create_access_token(
        data={"sub":user["username"]}, expires_delta=timedelta(minutes=30)
        
    )
    return {"access_token":access_token,"token_type":"bearer"}
    
    
if __name__ == "__main__":
        
    print('[O.K]')