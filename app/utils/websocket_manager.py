from typing import List, Dict
from fastapi import WebSocket, WebSocketDisconnect
from app.database.connection import mensajes_collection
from datetime import datetime
from app.utils.security import encrypt_message , decrypt_message


class ConnectionManager:
    """Gestiona las conexiones websocket activas"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.active_users: Dict[str,WebSocket] = {}
        
        
    async def store_message(self, username:str , message:str, to:str = None):
        
        """
        Guarda los mensajes en MongoDB, cifrando solo los mensajes de los usuarios.
        Ahora incluye soporte para mensajes privados con destinatario (to).
        """

        if message.startswith("🔵") or message.startswith("🔴"):
            encrypted_message = message  # No cifrar mensajes del sistema
        else:
            encrypted_message = encrypt_message(message)

        await mensajes_collection.insert_one({
            "from": username,
            "to": to,  # Esto puede ser None (mensaje público)
            "message": encrypted_message,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    async def connect(self,websocket:WebSocket, username:str):
        
        """
        Acepta una nueva conexion websocket
        
        """
        
        await websocket.accept()
        self.active_connections.append(websocket)
        self.active_users[username] = websocket
               
    async def disconnect(self, websocket: WebSocket, username:str):
        
        """
        Elimina una conexion websocket cuando un usuario se desconecta
        
        """
        
        
        self.active_connections.remove(websocket)
        self.active_users.pop(username,None)
           
    async def broadcast(self,username:str, message:str):
        
        """
        Envia un mensaje de broadcast a todos los usuarios conectados y lo guarda en AMongo ATLAS
        
        """
        await self.store_message(username, message)

        to_remove = []
        for connection in self.active_connections:
            try:
                await connection.send_json({
                    "username": username,
                    "message": message,
                    "timestamp": datetime.utcnow().isoformat()
                })
            except Exception:
                to_remove.append(connection)

        for conn in to_remove:
            self.active_connections.remove(conn)
           
    async def send_private_message(self, message:str, to_username:str):
        websocket = self.active_users.get(to_username)
        if websocket:
            await websocket.send_text(message)
            
    async def get_recent_messages(self, limit:int = 20):
        """
        Recumera los ultimos n mensajes almacenados en la coleccion
        
        """
        
        cursor = mensajes_collection.find().sort("timestamp",-1).limit(limit)
        messages = []
        
        async for doc in cursor:
            decrypted_message = doc["message"]
            #!Desencriptar solo si NO ES mensaje del sistema:
            if not decrypted_message.startswith("🔵") and not decrypted_message.startswith("🔴"):
                decrypted_message = decrypt_message(decrypted_message)
                
            messages.append({
                
                "from": doc.get("from") or doc.get("username"),
                "to": doc.get("to"),
                "message": decrypted_message,
                "timestamp": doc["timestamp"]
                
            })
        
            return list(reversed(messages))  #! OJO!! Para que estén en orden cronológico normal
    

manager = ConnectionManager()
    