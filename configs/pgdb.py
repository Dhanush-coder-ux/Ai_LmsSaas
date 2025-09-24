from sqlalchemy.ext.asyncio import async_sessionmaker,create_async_engine
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv('NEON_DB_URL')

ENGINE = create_async_engine(DB_URL)
SessionLocal = async_sessionmaker(ENGINE)
Base = declarative_base()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
