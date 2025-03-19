from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from app.utils.websocket_manager import manager
from app.utils.jwt import verify_access_token

router = APIRouter()


@router.websocket("ws/chat")
async def websocket_endpoint(websocket: WebSocket, token:str):
    """Maneja la conexion websocket con el token JWT"""
    
    #!Priumero validamos el token JWS antes de aceptar ninguna conexion
    
    payload = verify_access_token(token)
    
    if payload is None:
        await websocket.close(code=1008)
        return 
    
    username = payload.get("sub") #!-> extraemos asi el nombre de usuario del payload del token
    
    await manager.connect(websocket)
    await manager.broadcast(f"[:)] {username} se acaba de unir al chat.")
    
    try:
        while True:
            message = await websocket.receive_text()
            await manager.broadcast(f"{username}:{message}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"[):] {username} se ha desconectado del chat.")
        
        """

        Explicación:

        Autenticamos con el token JWT.
        Si el token es válido, extraemos el username del payload JWT.
        Conectamos al usuario y notificamos su entrada.
        Escuchamos mensajes y los reenviamos a todos los conectados.
        Si el usuario se desconecta, lo eliminamos y notificamos a los demás.


        """