from fastapi import HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession
from utils.genai_access_teacher import TeacherGainAIResponse
from models.teacher_models import TeacherFile, TeacherImage
from sqlalchemy import select
from datetime import datetime,timezone


class __TeacherController:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.genai = TeacherGainAIResponse() 
        self.file_table = TeacherFile
        self.image_table = TeacherImage


class TeacherCrud(__TeacherController):

    async def upload_file_docs(self,  teacher_id ,file_bytes, file_name, question):
        try:
            ai_answer =  self.genai.upload_and_ask(file_bytes, file_name, question)
            add_file = self.file_table(
                teacher_id = teacher_id,
                file_name=file_name,
                ai_response=ai_answer,
                created_at=datetime.now(tz=timezone.utc)
            )
            self.db.add(add_file)
            await self.db.commit()
            return {"Successfully added!"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Something went wrong while reading pdf: {e}")
        
    async def pull_file(self, teacher_id:str):
        try:
            result = (await self.db.execute(
                select(self.file_table).where(self.file_table.id == teacher_id)
            )
          ).scalars().first()
            if not result:
                raise HTTPException(status_code=404, detail="File not found")
            return {"file_response": result.ai_response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching file: {str(e)}")
        
    async def upload_image(self,teacher_id, image_byte, image_name, question):
        try:
            ai_answer = self.genai.uploadimage_and_ask(image_byte, image_name, question)
            add_image = self.image_table(
                 teacher_id = teacher_id,
                image_name=image_name,
                ai_response=ai_answer,
                created_at=datetime.now(tz=timezone.utc)
            )
            self.db.add(add_image)
            await self.db.commit()
            return f'Successfully added!'
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Something went wrong while reading image: {e}")
    
    async def pull_image(self, teacher_id:str):
        try:
            result = (await self.db.execute(
                select(self.image_table).where(self.image_table.id == teacher_id)
            )
          ).scalars().first()
            if not result:
                raise HTTPException(status_code=404, detail="Image not found")
            return {"image_response": result.ai_response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching image: {str(e)}")