from fastapi import FastAPI
from  routers import student_routes,teacher_routes, login_routes
from configs.pgdb import Base,ENGINE
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app:FastAPI):
    try:
        async with ENGINE.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("fastapi started-------->")
        yield
    except Exception as e:
        print(f"Error during startup: {e}")
    finally:
        print('server shutdown')

app = FastAPI(lifespan=lifespan)






app.include_router(teacher_routes.router)
app.include_router(student_routes.router)
app.include_router(login_routes.router)