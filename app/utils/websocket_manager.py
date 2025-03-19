from typing import List
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    """Gestiona las conexiones websocket activas"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        
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
        
        
    async def broadcast(self, message:str):
        
        """
        Envia un mensaje de broadcast a todos los usuarios conectados
        
        """
        
        for connection in self.active_connections:
            await connection.send_text(message)
            
        
#!Instancia del gestor de conexiones:
manager = ConnectionManager()
    