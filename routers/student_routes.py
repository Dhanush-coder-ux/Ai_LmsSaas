from fastapi import APIRouter, UploadFile, Form, Depends
from configs.pgdb import get_db
from crud.students import StudentCrud
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    tags=['studentscrud']
)

@router.post('/uploaddocs')
async def create_file_response(
    file: UploadFile, 
    question: str = Form(...), 
    db: AsyncSession = Depends(get_db)

): 
    file_bytes=await file.read()
    file_name =file.filename
    return await StudentCrud(db=db).upload_files_and_images( file_bytes,file_name, question)


@router.post('/imagegen')
async def create_image(
    promp: str = Form(...),
    db:AsyncSession = Depends(get_db)
):
    return await StudentCrud(db=db).flowchart_generation(promp)
