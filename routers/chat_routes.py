from fastapi import WebSocket , WebSocketDisconnect , APIRouter
from utils.websocket_manager import ConnectionManager
from utils.uniqueid import create_unique_id
import json
from utils.encryption import encrypt_message,decrypt_message
from icecream import ic

router = APIRouter(
    tags=['Websocket']
)

manager = ConnectionManager()

@router.websocket('/ws')
async def websocket_connection( ws : WebSocket):
    user_id=create_unique_id('ws')
    await manager.connect(ws=ws,user_id=user_id)
    await manager.broadcast(f'{''}joined room {user_id}')

    try:
        while True:
            data = await ws.receive_text()
            encrypted_msg = encrypt_message(data)
            ic("encrypted",encrypted_msg)
            decrypted_msg = decrypt_message(encrypted_msg)
            ic("decrypted",decrypted_msg)
            data =json.loads(decrypted_msg)

            if isinstance(data,dict):
                incoming_uid=data.get('user_id')
                if incoming_uid:
                    await manager.send_personal_message(message=f"user:{data}",user_id=incoming_uid)
                else:
                    await manager.broadcast(f"From brodcast user id not found: {data}")
            else:
                await manager.broadcast(f"From brodcast : {data}")
    except WebSocketDisconnect:
        manager.disconnect(user_id=user_id)
        await manager.broadcast(f'user left chat {user_id}')
    except RuntimeError:
        await manager.disconnect(user_id=user_id)
    