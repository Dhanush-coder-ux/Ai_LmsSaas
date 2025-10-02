from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, DateTime
from configs.pgdb import Base
from datetime import datetime
import uuid


class Teacher(Base):
    __tablename__ = "teachers"
    
    teacher_id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    profile_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    prompts = relationship("TeacherPrompt", back_populates="teacher", cascade="all, delete-orphan")
    files = relationship("TeacherFile", back_populates="teacher", cascade="all, delete-orphan")
    images = relationship("TeacherImage", back_populates="teacher", cascade="all, delete-orphan")

class TeacherPrompt(Base):
    __tablename__ = "teacher_prompts"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    teacher_id = Column(String, ForeignKey("teachers.teacher_id", ondelete="CASCADE"))
    prompt = Column(String, nullable=False)
    ai_response = Column(String)  
    created_at = Column(DateTime, default=datetime.utcnow)

    teacher = relationship("Teacher", back_populates="prompts")


class TeacherFile(Base):
    __tablename__ = 'teacher_files'
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    teacher_id = Column(String, ForeignKey("teachers.teacher_id", ondelete="CASCADE"))
    file_name = Column(String, nullable=False)
    ai_response = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    teacher = relationship("Teacher", back_populates="files")

class TeacherImage(Base):
    __tablename__ = 'teacher_images'
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    teacher_id = Column(String, ForeignKey("teachers.teacher_id", ondelete="CASCADE"))
    ai_response = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    teacher = relationship("Teacher", back_populates="images")