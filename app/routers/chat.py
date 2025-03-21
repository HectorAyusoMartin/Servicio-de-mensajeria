from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from app.utils.websocket_manager import manager
from app.utils.jwt import verify_access_token


router = APIRouter()


@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, token: str):
    
    user_data = verify_access_token(token)
    if not user_data:
        await websocket.close()
        return

    username = user_data["sub"]
    await manager.connect(websocket, username)
    
    #!Recuperando los mensajes..
    recent_messages = await manager.get_recent_messages()
    #!Enviando los mensajes solo al suaurio que se acaba de conectar..
    for msg in recent_messages:
        await websocket.send_json({
            
            "from":msg["from"],
            "to":msg["to"],
            "message":msg["message"],
            "timestamp":msg["timestamp"]
        })
    
    await manager.broadcast("sistema", f"🔵 {username} ha entrado")

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type", "public")
            message = data.get("message")

            if msg_type == "private":
                to_user = data.get("to")
                await manager.send_private_message(
                    f"(Privado de {username}): {message}",
                    to_user
                )
                await manager.store_message(username, message, to=to_user)
            else:
                await manager.broadcast(username, message)

    except WebSocketDisconnect:
        manager.disconnect(websocket, username)
        await manager.broadcast("sistema", f"🔴 {username} ha salido")
        
      