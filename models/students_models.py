from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, Text,Float,Integer
from sqlalchemy.orm import relationship
from configs.pgdb import Base


class Students(Base):
    __tablename__ = "students"
    
    student_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    profile_url = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True))

    # Relationships
    prompts = relationship("StudentPrompt", back_populates="student", cascade="all, delete-orphan")
    files = relationship("StudentFile", back_populates="student", cascade="all, delete-orphan")
    flowcharts = relationship("StudentFlowchart", back_populates="student", cascade="all, delete-orphan")
    roadmaps = relationship("StudentRoadmap", back_populates="student", cascade="all, delete-orphan")
    image = relationship('StudentImage',back_populates="student",cascade="all, delete-orphan")
    quizes = relationship("StudentActivitys",back_populates="student",cascade="all,delete-orphan")
    assigned_tasks = relationship("TaskAssignment", back_populates="student", cascade="all, delete-orphan")



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

class StudentImage(Base):
    __tablename__ = 'student_images'
    
    id = Column(String, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id", ondelete="CASCADE"))
    image_name = Column(String,nullable=False)
    ai_response = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True))

    student = relationship("Students", back_populates="image")


class StudentActivitys(Base):
    __tablename__ = "student_activity"
    id = Column(String, primary_key=True)
    student_id = Column(String, ForeignKey("students.student_id",ondelete="CASCADE"))
    topic = Column(String)
    duration = Column(Integer,nullable=False)
    accuracy = Column(Float, nullable=True)
    timestamp = Column(TIMESTAMP(timezone=True))

    student = relationship("Students",back_populates="quizes")