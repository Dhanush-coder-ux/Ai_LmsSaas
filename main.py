from fastapi import FastAPI
from  routers.student_routes import router

app = FastAPI()






app.include_router(router)