from fastapi import FastAPI,Response,UploadFile,Form
from  routers.student_routes import router
app = FastAPI()




@app.get('/summa')
def summa():
    res=Response("vaalaka baji")
    res.set_cookie('tesing',value='oh my god',httponly=True)
    return res

app.include_router(router)