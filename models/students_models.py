from sqlalchemy import Column, Integer, String
from configs.pgdb import Base

class Student(Base):
    __tablename__ = "students"