from fastapi import APIRouter, UploadFile, Form, Depends,HTTPException,File,BackgroundTasks
from configs.pgdb import get_db
from crud.students import StudentCrud
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    tags=['studentscrud']
)

# File upload and question form data

@router.post('/upload-docs/{student_id}')
async def create_file_response(student_id: str,file: UploadFile=File(...),question: str = Form(...), db: AsyncSession = Depends(get_db)): 
    file_bytes=await file.read()
    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds the 5MB limit.")
    file_name =file.filename
    return  await StudentCrud(db=db).upload_files_and_images(file_bytes=file_bytes, file_name=file_name, question=question, student_id=student_id)


@router.get('/get-answer/{id}')
async def get_answer( id: str, db: AsyncSession = Depends(get_db)):
    return await StudentCrud(db=db).pull_answer(id)

# Resume upload and retrieval

@router.post('/upload-resume/{student_id}')
async def create_file_response(file: UploadFile,student_id: str,db: AsyncSession = Depends(get_db)): 
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds the 5MB limit.")
    file_name = file.filename
    return await StudentCrud(db=db).upload_resume_to_ai(file_bytes=contents, file_name=file_name,student_id=student_id)

@router.get('/get-resume/{id}')
async def get_resume(id: str,db: AsyncSession = Depends(get_db)):
    return await StudentCrud(db=db).pull_resume(id)

# Image generation and retrieval

@router.post('/image-gen/{student_id}')
async def create_image(student_id:str,prompt: str = Form(...),db:AsyncSession = Depends(get_db)):
    return await StudentCrud(db=db).flowchart_generation(student_id=student_id,prompt=prompt)

@router.get('/get-image/{id}')
async def get_image(id: str,db: AsyncSession = Depends(get_db)):
    return await StudentCrud(db=db).pull_flowchart(id)


# Roadmap generation and retrieval

@router.post('/roadmap-gen/{student_id}')
async def create_roadmap( student_id:str, prompt: str = Form(...),db:AsyncSession =Depends(get_db)):
    return await StudentCrud(db=db).roadmap_generation(prompt=prompt,student_id=student_id)

@router.get('/get-roadmap/{id}')
async def get_roadmap( id: str, db: AsyncSession = Depends(get_db)):
    return await StudentCrud(db=db).pull_roadmap(id)