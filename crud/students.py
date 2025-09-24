from fastapi import HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession
from configs.genai import upload_and_ask,generate_flowchart

class __StudentController:
    def __init__(self, db: AsyncSession):
        self.db = db
class StudentCrud(__StudentController):

    async def upload_files_and_images(self,file_bytes,file_name, question):
        try:
            answer =upload_and_ask(file_bytes,file_name, question)
            return {"answer": answer}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Something went wrong while uploading the file: {e}")
    
    async def flowchart_generation(self,prompt):
        try:
            chart= generate_flowchart(prompt)
            return chart
        except Exception as e:
            raise HTTPException (status_code=500, detail=f"Something went wrong while generating the image: {e}")
