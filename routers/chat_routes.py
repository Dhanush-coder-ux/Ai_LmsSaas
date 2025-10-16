from fastapi import WebSocket, WebSocketDisconnect, APIRouter, HTTPException
from utils.websocket_manager import ConnectionManager
import json
from utils.encryption import encrypt_message, decrypt_message
from icecream import ic
from configs.pgdb import get_db
from security.token_verify import verify_websocket_token

router = APIRouter(tags=["Websocket"])
manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_connection(ws: WebSocket):
    token = ws.query_params.get("token")
    if not token:
        await ws.close(code=1008, reason="Missing token")
        return

    async for db in get_db():
        try:
            user = await verify_websocket_token(token, db)
        except HTTPException as e:
            await ws.close(code=1008, reason=e.detail)
            return
        break 

    user_id = user["user_id"]
    await manager.connect(ws=ws, user_id=user_id)
    await manager.broadcast(f"{user['name']} joined room ({user_id})")

    try:
        while True:
            data = await ws.receive_text()
            encrypted_msg = encrypt_message(data)
            ic("encrypted", encrypted_msg)
            decrypted_msg = decrypt_message(encrypted_msg)
            ic("decrypted", decrypted_msg)
            data = json.loads(decrypted_msg) 

            if isinstance(data, dict):
                incoming_uid = data.get("user_id")
                if incoming_uid:
                    await manager.send_personal_message(
                        message=f"user:{data}", user_id=incoming_uid
                    )
                else:
                    await manager.broadcast(f"Broadcast: user id not found: {data}")
            else:
                await manager.broadcast(f"Broadcast: {data}")

    except WebSocketDisconnect:
        manager.disconnect(user_id=user_id)
        await manager.broadcast(f"User left chat {user_id}")
    except RuntimeError:
        manager.disconnect(user_id=user_id)


