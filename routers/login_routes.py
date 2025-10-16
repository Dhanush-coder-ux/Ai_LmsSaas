import httpx
from fastapi import APIRouter,HTTPException,Depends,BackgroundTasks
from fastapi.responses import RedirectResponse
from security.token_verify import get_current_user
from configs.debuggers import client_secrets,api_key,debuggers_baseurl
import jwt
from utils.uniqueid import create_unique_id
from security.token_generations import TokenData
from models.students_models import Students
from utils.uniqueid import create_unique_id
from datetime import datetime,timezone
from configs.pgdb import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from icecream import ic
from sqlalchemy import select
from utils.email_sending import send_email

router = APIRouter(
    tags=['Login']
)

token = TokenData()


@router.get('/login')
async def login():
    async with httpx.AsyncClient() as redirect:
        res = await redirect.post(url=f'{debuggers_baseurl}/auth',json={'apikey':api_key},timeout=80)
    print(res.text)
    if res.status_code == 200:
        print(res.text)
        return RedirectResponse(res.json()['login_url'],status_code=302)
    else:
        raise HTTPException(status_code=res.status_code,detail=f'{res.text}')  
       
@router.get('/redirect')
async def redirect_url(
    background_tasks:BackgroundTasks,
    code:str,
    db:AsyncSession=Depends(get_db),
):
    async with httpx.AsyncClient() as redirect:
        print(client_secrets)
        res = await redirect.post(url=f'{debuggers_baseurl}/auth/authenticated-user',json={'code':code,'client_secret':client_secrets},timeout=80)
    if res.status_code == 200:
        infos = jwt.decode(res.json()['token'],options={"verify_signature": False})
        ic(infos)
        id  = create_unique_id(infos['name'])  
        token =TokenData
        access_token = token.create_access_token({
            'user_id':id,
            'email':infos['email']
            })
        refresh_token = token.create_refresh_token({
            'user_id':id,
            'email':infos['email']
            })

        ic(access_token)
        check =  await db.execute(
            select(
                Students
            ).where(Students.email == infos['email']))
        response = RedirectResponse(url=f'https://authdebuggers.vercel.app/?access_token={access_token}&refresh_token={refresh_token}&name={infos['name']}&profile=https://google.com/',status_code=302)
        if not check.scalar_one_or_none():
            
            adduser = Students(
                student_id = id,
                name = infos['name'],
                email = infos['email'],
                profile_url = infos['profile_picture'],
              
                created_at =datetime.now(tz=timezone.utc)
            )
            db.add(adduser)
            await db.commit()
            background_tasks.add_task(
            send_email,
            to_email=infos['email'],
            subject="🤖 Welcome to Sensei.ai — The Future of Learning",
            template_name="welcome.html",
            context={
                "name": infos['name'],
                "dashboard_url": f"https://sensei-ai.vercel.app/dashboard?user={infos['email']}"

            }
        )
        return response

@router.get('/me')
async def get_me(current_user: dict = Depends(get_current_user)):
    return {'message':'Authenticated !',"user":current_user['profile_url']}
