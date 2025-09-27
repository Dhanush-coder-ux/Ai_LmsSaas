from fastapi import FastAPI
from  routers import student_routes,teacher_routes

app = FastAPI()




app.include_router(teacher_routes.router)
app.include_router(student_routes.router)
