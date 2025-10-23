from sqlalchemy.ext.asyncio import AsyncSession
from security.token_generations import TokenData , ACCESS_TOKEN_KEY
from fastapi import HTTPException,Depends
from sqlalchemy import select
from models.students_models import Students
from models.teacher_models import Teacher
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



async def get_current_user(credentials: credintials, db: AsyncSession = Depends(get_db)):
    try:
        payload = token.decode_jwt(credentials.credentials, ACCESS_TOKEN_KEY)
        if not isinstance(payload, dict):
            raise HTTPException(status_code=401, detail="Invalid token")
        
    
        user_student = (await db.execute(
            select(Students).where(Students.email == payload.get("email"))
        )).scalar_one_or_none()

        user_teacher = (await db.execute(
            select(Teacher).where(Teacher.email == payload.get("email"))
        )).scalar_one_or_none()

        if not user_student and not user_teacher:
            raise HTTPException(status_code=404, detail="User not found")
        
        if user_student:
            user_obj = user_student
            role = "student"
            user_id = user_student.student_id
        else:
            user_obj = user_teacher
            role = "teacher"
            user_id = user_teacher.teacher_id

        return {
            "user_id": user_id,
            "name": user_obj.name,
            "email": user_obj.email,
            "role": role,
            "profile_url": getattr(user_obj, "profile_url", None)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong while verifying user credentials: {e}")

    

        




         
