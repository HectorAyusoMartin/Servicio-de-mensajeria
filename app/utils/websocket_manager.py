from typing import List
from fastapi import WebSocket, WebSocketDisconnect
from app.database.connection import mensajes_collection
from datetime import datetime
from app.utils.security import encrypt_message


class ConnectionManager:
    """Gestiona las conexiones websocket activas"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        
    async def store_message(self, username:str , message:str):
        
        """
        Guardamos el mensaje en Mongo DB ATLAS
        
        """
        
        encrypted_message = encrypt_message(message)
        await mensajes_collection.insert_one({
        "username": username,
        "message": encrypted_message,
        "timestamp": datetime.utcnow().isoformat()
        })
        
        
    async def connect(self,websocket:WebSocket):
        
        """
        Acepta una nueva conexion websocket
        
        """
        
        await websocket.accept()
        self.active_connections.append(websocket)
        
    async def disconnect(self, websocket: WebSocket):
        
        """
        Elimina una conexion websocket cuando un usuario se desconecta
        
        """
        
        
        self.active_connections.remove(websocket)
           
    async def broadcast(self,username:str, message:str):
        
        """
        Envia un mensaje de broadcast a todos los usuarios conectados y lo guarda en AMongo ATLAS
        
        """
        
        await self.store_message(username,message)
        
        
        
        for connection in self.active_connections:
            await connection.send_json({
                "username":username,
                "message":message,
                "timestamp":datetime.utcnow().isoformat()
            })
            
        
#!Instancia del gestor de conexiones:
manager = ConnectionManager()
    