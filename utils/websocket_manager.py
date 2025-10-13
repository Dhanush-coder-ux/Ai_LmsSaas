from typing import List,Dict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections:Dict[str, WebSocket] = {} #{'12345-6789-900:Websoctet} 

    async def connect(self,ws:WebSocket,user_id:str):
        await ws.accept()
        self.active_connections[user_id]=ws

    def disconnect(self,user_id:str):
        del self.active_connections[user_id]

    async def send_personal_message(self, message: str,user_id:str):
        connected_user_websocket=self.active_connections.get(user_id)
        print("all connected users : ",self.active_connections)
        print('this is connected user websocket : ',connected_user_websocket)
        if not connected_user_websocket:
            print('User doesnot connect in websocket')
            return
        await connected_user_websocket.send_text(message)
    
    async def broadcast(self, message : str):
        for key,value in self.active_connections.items():
            await value.send_text(message)