from fastapi import APIRouter, UploadFile, Form, Depends
from configs.pgdb import get_db
from crud.students import StudentCrud
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    tags=['studentscrud']
)
session_maker = AsyncSession()

@router.post('/upload-docs')
async def create_file_response(
    file: UploadFile, 
    question: str = Form(...), 
    db: AsyncSession = Depends(get_db)

): 
    file_bytes=await file.read()
    file_name =file.filename
    return await StudentCrud(db=db).upload_files_and_images( file_bytes,file_name, question)


@router.post('/image-gen')
async def create_image(
    prompt: str = Form(...),
    db:AsyncSession = Depends(get_db)
):
    return await StudentCrud(db=db).flowchart_generation(prompt)


@router.post('/roadmap-gen')
def create_roadmap(
    prompt: str = Form(...),
    db:AsyncSession =Depends(get_db)
):
    return  StudentCrud(db=db).roadmap_generation(prompt)