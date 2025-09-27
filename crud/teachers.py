from fastapi import HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession
from utils.genai_access_teacher import TeacherGainAIResponse

class __TeacherController:
    def __init__(self, db: AsyncSession):
        self.db = db
class TeacherCrud(__TeacherController):

    def upload_file_docs(self,file_bytes,file_name, question):
        try:
            ai_answer = TeacherGainAIResponse.upload_and_ask(file_bytes,file_name, question)
            return ai_answer
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"something went wrong while reading pdf{e}")
        
    def upload_image(self,image_byte,image_name,question):
        try:
            ai_answer = TeacherGainAIResponse.uploadimage_and_ask(image_byte,image_name,question)
            return ai_answer
        except Exception as e:
            raise HTTPException(status_code=500,detail=f'something went wromg while reading image{e}')
