import httpx
from fastapi import APIRouter,HTTPException
from fastapi.responses import RedirectResponse
from configs.debuggers import client_secrets,api_key,debuggers_baseurl
import jwt
from utils.uniqueid import create_unique_id
from security.token_generations import TokenData




router = APIRouter(
    tags=['/user-login']
)

token = TokenData()

@router.get('/login')
async def login():
    async with httpx.AsyncClient() as redirect:
        res = await redirect.post(url=f'{debuggers_baseurl}/auth',json={'apikey':api_key})
    if res.status_code == 200:
        return RedirectResponse(res.json(),status_code=302)
    else:
        raise HTTPException(status_code=res.status_code,detail=f'{res.text}')  
       
@router.get('/redirect')
async def redirect_url(code:str):
    async with httpx.AsyncClient() as redirect:
        res = await redirect.post(url=f'{debuggers_baseurl}/auth/authenticated-user',json={'code':code,'client_secret':client_secrets})
    if res.status_code == 200:
        infos = jwt.decode(res.json(),options={"verify_signature": False})
        print(infos)
        id = create_unique_id(infos['name'])
        access_token = token.create_access_token({'user_id':id})
        refresh_token = token.create_refresh_token({'user_id':id})
        response = RedirectResponse(url=f'',status_code=302)
        response.set_cookie(key='access_token',value=access_token)    
        response.set_cookie(key='refresh_token',value=refresh_token)    
        return response
    
        




         
