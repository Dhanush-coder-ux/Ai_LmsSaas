from fastapi import HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession
from utils.genai_access import GenAIResponse

class __StudentController:
    def __init__(self, db: AsyncSession):
        self.db = db
class StudentCrud(__StudentController):

    def upload_files_and_images(self,file_bytes,file_name, question):
        try:
            answer =GenAIResponse.upload_and_ask(file_bytes,file_name, question)
            return {"answer": answer}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Something went wrong while uploading the file: {e}")

    def upload_reumeto_ai(self,file_bytes,file_name):
        try:
            answer =GenAIResponse.upload_resume(file_bytes,file_name)
            return {"answer": answer}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Something went wrong while uploading the file: {e}")
    
    def flowchart_generation(self,prompt):
        try:
            chart= GenAIResponse.generate_flowchart(prompt)
            return chart
        
        except Exception as e:
            raise HTTPException (status_code=500, detail=f"Something went wrong while generating the image: {e}")
        
    def roadmap_generation(self,prompt):
        try:
            roadmap =GenAIResponse.generate_roadmap(prompt)
            return{"roadmap":roadmap}
        
        except Exception as e:
            raise HTTPException (status_code=500, detail=f"Something went wrong while generating the roadmap: {e}")
        

    
    
