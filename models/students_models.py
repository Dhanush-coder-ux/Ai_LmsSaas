from sqlalchemy import Column, Integer, String,ForeignKey,TIMESTAMP
from sqlalchemy.orm import relationship
from configs.pgdb import Base
from datetime import datetime


class Students(Base):
    __tablename__ = "students"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    profile_url = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False)

    creation = relationship("StudentCreation", back_populates="student", cascade="all, delete-orphan")



class StudentCreation(Base):
    __tablename__ = "students_creations"
    id = Column(String,primary_key=True,index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    prompt = Column(String, nullable=False)
    ai_response = Column(String)  
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)

    student = relationship("Students", back_populates="creation")





