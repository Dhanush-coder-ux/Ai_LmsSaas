from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, DateTime,Text,Boolean
from configs.pgdb import Base
from datetime import datetime
import uuid


class Teacher(Base):
    __tablename__ = "teachers"
    role = Column(String, default="teacher", nullable=False)
    teacher_id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    profile_url = Column(String)
    created_at = Column(DateTime(timezone=True))

    # Relationships
    prompts = relationship("TeacherPrompt", back_populates="teacher", cascade="all, delete-orphan")
    files = relationship("TeacherFile", back_populates="teacher", cascade="all, delete-orphan")
    images = relationship("TeacherImage", back_populates="teacher", cascade="all, delete-orphan")
    question_paper = relationship("TeacherQuestionFile",back_populates="teacher",cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="teacher", cascade="all, delete-orphan")


class TeacherPrompt(Base):
    __tablename__ = "teacher_prompts"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    teacher_id = Column(String, ForeignKey("teachers.teacher_id", ondelete="CASCADE"))
    prompt = Column(String, nullable=False)
    ai_response = Column(String)  
    created_at = Column(DateTime(timezone=True))

    teacher = relationship("Teacher", back_populates="prompts")


class TeacherFile(Base):
    __tablename__ = 'teacher_files'
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    teacher_id = Column(String, ForeignKey("teachers.teacher_id", ondelete="CASCADE"))
    file_name = Column(String, nullable=False)
    ai_response = Column(String)
    created_at = Column(DateTime(timezone=True))

    teacher = relationship("Teacher", back_populates="files")

class TeacherQuestionFile(Base):
    __tablename__ = 'teacher_questions'
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    teacher_id = Column(String, ForeignKey("teachers.teacher_id", ondelete="CASCADE"))
    file_name = Column(String, nullable=False)
    ai_response = Column(String)
    created_at = Column(DateTime(timezone=True))

    teacher = relationship("Teacher", back_populates="question_paper")

class TeacherImage(Base):
    __tablename__ = 'teacher_images'
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    teacher_id = Column(String, ForeignKey("teachers.teacher_id", ondelete="CASCADE"))
    image_name = Column(String,nullable=False)
    ai_response = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True))

    teacher = relationship("Teacher", back_populates="images")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String,primary_key=True,index=True)
    teacher_id = Column(String,ForeignKey("teachers.teacher_id",ondelete="CASCADE"))
    title = Column(Text,nullable=False)
    describtion = Column(Text,nullable=False)
    due_date = Column(DateTime,nullable=False)
    created_at = Column(DateTime(timezone=True))

    teacher = relationship("Teacher", back_populates="tasks")
    assigned_students = relationship("TaskAssignment", back_populates="task")

class TaskAssignment(Base):
    __tablename__ = "task_assignments"

    id = Column(String, primary_key=True, index=True)
    task_id = Column(String, ForeignKey("tasks.id"))
    student_id = Column(String, ForeignKey("students.student_id"))
    assigned_at = Column(DateTime(timezone=True))
    is_completed = Column(Boolean)
    submission_link = Column(String(500), nullable=True)
    feedback = Column(Text, nullable=True)

    task = relationship("Task", back_populates="assigned_students")
    student = relationship("Students", back_populates="assigned_tasks")
