from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.students_models import StudentPrompt, StudentFile, StudentFlowchart, StudentRoadmap,StudentImage
from datetime import datetime,timezone
from utils.uniqueid import create_unique_id
import json
from utils.genai_access import GenAIResponse


class __StudentController:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.genai = GenAIResponse()
        self.table = StudentPrompt
        self.resume = StudentFile
        self.flowchart = StudentFlowchart
        self.roadmap = StudentRoadmap
        self.image = StudentImage

class StudentCrud(__StudentController):
    
    async def upload_files_and_images(self, student_id, file_bytes, file_name, question):
        try:
            answer = self.genai.upload_and_ask(file_bytes, file_name, question)
            if not answer:
                raise HTTPException(status_code=404, detail="No answer found for the given question.")    
            add_answer = self.table(
                ids=create_unique_id(file_name),
                student_id=student_id,
                prompt=question,
                ai_response=answer,
                created_at=datetime.now(tz=timezone.utc)
            )
            self.db.add(add_answer)
            await self.db.commit()
            return {"message": "Successfully added!"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error while uploading file: {str(e)}")


    async def pull_answer(self, id: str):
        try:
            result = (await self.db.execute(
                select(self.table.ai_response).where(self.table.student_id == id)  
            )
            ).mappings().all()
            if not result:
                raise HTTPException(status_code=404, detail="Answer not found")
            return {"answer": result}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")



    async def upload_resume_to_ai(self, student_id: str, file_bytes, file_name: str):
        try:
            answer = self.genai.upload_resume(file_bytes, file_name)
            if not answer:
                raise HTTPException(status_code=404, detail="No answer found for the given resume.")            
            add_resume = self.resume(
                id=create_unique_id(file_name),
                student_id=student_id,
                file_name=file_name,
                ai_response=answer,
                created_at=datetime.now(tz=timezone.utc)
            )
            self.db.add(add_resume)
            await self.db.commit()
            return {"message": "Resume added successfully!"}
        except HTTPException:
            raise  
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error uploading resume: {str(e)}")



    async def pull_resume(self, id: str):
        try:
            result =( await self.db.execute(
                select(self.resume.ai_response).where(self.resume.student_id == id)
            )).mappings().all()
            if not result:
                raise HTTPException(status_code=404, detail="Resume not found")
            return {"resume": result}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching resume: {str(e)}")



    async def flowchart_generation(self, student_id: str, prompt: str):
        try:
            chart = self.genai.generate_flowchart(prompt)
            chart =json.dumps(chart)
            add_chart = self.flowchart(
                id=create_unique_id(prompt),
                student_id=student_id,
                prompt=prompt,
                ai_response=chart,
                created_at=datetime.now(tz=timezone.utc)
            )
            self.db.add(add_chart)
            await self.db.commit()
            return {"message": "Flowchart added successfully!"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating flowchart: {str(e)}")



    async def pull_flowchart(self, id: str):
        try:
            result = (await self.db.execute(
                select(self.flowchart.ai_response).where(self.flowchart.student_id == id)
            )
             ).mappings().all()
            if not result:
                raise HTTPException(status_code=404, detail="Flowchart not found")
            return {"flowchart": result}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching flowchart: {str(e)}")



    async def roadmap_generation(self, student_id: str, prompt: str):
        try:
            roadmap = self.genai.generate_roadmap(prompt)
            add_roadmap = self.roadmap(
                id=create_unique_id(prompt),
                student_id=student_id,
                prompt=prompt,
                ai_response=roadmap,
                created_at=datetime.now(tz=timezone.utc)
            )
            self.db.add(add_roadmap)
            await self.db.commit()
            return {"message": "Roadmap added successfully!"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating roadmap: {str(e)}")



    async def pull_roadmap(self, id: str):
        try:
            result = (await self.db.execute(
                select(self.roadmap.ai_response).where(self.roadmap.student_id == id)
            )
          ).mappings().all()
            if not result:
                raise HTTPException(status_code=404, detail="Roadmap not found")
            return {"roadmap": result}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching roadmap: {str(e)}")



    async def image_understandings(self,student_id ,image_byte,question,image_name):
        try:
            addimage = self.genai.uploadimage_and_ask(image_byte,image_name,question)
            addimage_response =  self.image(
                id = create_unique_id(image_name),
                student_id = student_id,
                image_name = image_name,
                 ai_response =addimage,
                 created_at = datetime.now(tz=timezone.utc) 
            )
            self.db.add(addimage_response)
            await self.db.commit()
            return f'successfully addedd !'
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500,detail=f'something went wrong while adding image{e}')
