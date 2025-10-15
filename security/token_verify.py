from sqlalchemy.ext.asyncio import AsyncSession
from security.token_generations import TokenData , ACCESS_TOKEN_KEY
from fastapi import HTTPException,Depends
from sqlalchemy import select
from models.students_models import Students
from typing import Annotated
from configs.pgdb import get_db
from security.token_generations import TokenData
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer

token = TokenData()
security = HTTPBearer()
credintials = Annotated[ HTTPAuthorizationCredentials, Depends(security)]

async def verify_websocket_token(token: str, db: AsyncSession):
    payload = TokenData.decode_jwt(token=token, key=ACCESS_TOKEN_KEY)
    if not isinstance(payload, dict):
        raise HTTPException(status_code=401, detail="Invalid token")

    user = (
        await db.execute(select(Students).where(Students.email == payload.get("email")))
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": user.student_id,
        "name": user.name,
        "email": user.email,
        "profile_url": getattr(user, "profile_url", None),
    }



async def get_current_user( credintials : credintials ,db:AsyncSession=Depends(get_db)):
    try:
        payload = token.decode_jwt(credintials.credentials,ACCESS_TOKEN_KEY)
        print(type(payload))
        if not isinstance(payload,dict):
            raise HTTPException(status_code=401,detail='invalid token')
        
        user = (await db.execute(
            select(Students).where(
                Students.email == payload.get("email")
            )
        )).scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404,detail='user not found')
        return {
            "user_id":user.student_id,
            "name":user.name,
            "email":user.email,
            "profile_url":getattr(user,"profile_url",None)
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'something went wrong while verify user credenials{e}')
    

        




         
