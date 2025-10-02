import uuid
from fastapi import HTTPException


def create_unique_id(data:str):
    try:
        return str(uuid.uuid5(uuid.uuid4(),data))
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"seomething went wrong while creating unique id {e}")