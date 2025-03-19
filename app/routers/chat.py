from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from app.utils.websocket_manager import manager
from app.utils.jwt import verify_access_token

router = APIRouter()


@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    """Maneja la conexión WebSocket con autenticación JWT."""
    
    # Extraer el token desde la URL manualmente
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008)  # 1008 = Policy Violation
        return

    # Validar el token JWT
    payload = verify_access_token(token)
    if payload is None:
        await websocket.close(code=1008)
        return
    
    username = payload.get("sub")  # Extraer el nombre de usuario del token

    await manager.connect(websocket)
    await manager.broadcast(f"🔵 {username} se ha unido al chat.")

    try:
        while True:
            message = await websocket.receive_text()
            await manager.broadcast(f"{username}: {message}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"🔴 {username} se ha desconectado.")
        
        """

        Explicación:

        Autenticamos con el token JWT.
        Si el token es válido, extraemos el username del payload JWT.
        Conectamos al usuario y notificamos su entrada.
        Escuchamos mensajes y los reenviamos a todos los conectados.
        Si el usuario se desconecta, lo eliminamos y notificamos a los demás.


        """