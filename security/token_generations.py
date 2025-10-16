import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from configs.cryptography import load_dotenv,os

load_dotenv()


ACCESS_TOKEN_KEY = os.getenv("ACCESS_TOKEN_KEY ")
REFRESH_TOKEN_KEY =  os.getenv("REFRESH_TOKEN_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXP_TIME = os.getenv("ACCESS_TOKEN_EXP_TIME")
REFRESH_TOKEN_DAY =  os.getenv("REFRESH_TOKEN_DAY ")      


class TokenData:

    def create_access_token(data: dict):
        payload = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXP_TIME)
        payload["exp"] = expire
        return jwt.encode(payload, key=ACCESS_TOKEN_KEY, algorithm=ALGORITHM)

 
    def create_refresh_token(data: dict):
        payload = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_DAY)
        payload["exp"] = expire
        return jwt.encode(payload, key=REFRESH_TOKEN_KEY, algorithm=ALGORITHM)
    @staticmethod
    def decode_jwt(token: str, key: str):
        try:
            decoded_data = jwt.decode(token, key=key, algorithms=[ALGORITHM])
            return decoded_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}")

    def get_access_token(refresh_token: str):
        decoded_data = TokenData.decode_jwt(refresh_token, REFRESH_TOKEN_KEY)
        decoded_data.pop("exp", None)  
        return TokenData.create_access_token(decoded_data)



