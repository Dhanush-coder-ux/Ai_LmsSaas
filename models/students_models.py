from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from configs.pgdb import Base
from datetime import datetime


class Students(Base):
    __tablename__ = "students"
    
    student_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    profile_url = Column(String)
    created_at = Column(TIMESTAMP(timezone=True))

    # Relationships
    prompts = relationship("StudentPrompt", back_populates="student", cascade="all, delete-orphan")
    files = relationship("StudentFile", back_populates="student", cascade="all, delete-orphan")
    flowcharts = relationship("StudentFlowchart", back_populates="student", cascade="all, delete-orphan")
    roadmaps = relationship("StudentRoadmap", back_populates="student", cascade="all, delete-orphan")


class StudentPrompt(Base):
    __tablename__ = "student_prompts"
    
    ids = Column(String, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id", ondelete="CASCADE"))
    prompt = Column(String, nullable=False)
    ai_response = Column(String)  
    created_at = Column(TIMESTAMP(timezone=True))

    student = relationship("Students", back_populates="prompts")


class StudentFile(Base):
    __tablename__ = 'student_files'
    
    id = Column(String, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id", ondelete="CASCADE"))
    file_name = Column(String, nullable=False)
    ai_response = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True))

    student = relationship("Students", back_populates="files")


class StudentFlowchart(Base):
    __tablename__ = 'student_flowcharts'
    
    id = Column(String, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id", ondelete="CASCADE"))
    prompt = Column(Text, nullable=False)
    ai_response = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True))

    student = relationship("Students", back_populates="flowcharts")


class StudentRoadmap(Base):
    __tablename__ = 'student_roadmaps'
    
    id = Column(String, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id", ondelete="CASCADE"))
    prompt = Column(Text, nullable=False)
    ai_response = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True))

    student = relationship("Students", back_populates="roadmaps")
