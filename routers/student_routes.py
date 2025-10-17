from fastapi import APIRouter, UploadFile, Form, Depends,HTTPException,File
from configs.pgdb import get_db
from Controlers.students import StudentCrud
from sqlalchemy.ext.asyncio import AsyncSession
from security.token_verify import get_current_user
from typing import Annotated
from crud.students_crud import StudentActivity



router = APIRouter(
    tags=['studentscrud']
)


current_user = Annotated[dict,Depends(get_current_user)]
db = Annotated[AsyncSession,Depends(get_db)]




# this is a students ai access routes ...........................>

# File upload and question form data

@router.post('/upload-docs/{student_id}')
async def create_file_response(
    student_id: str,
    db:db,
    user : current_user,
    file: UploadFile=File(...),
    question: str = Form(...), 
): 
    file_bytes=await file.read()
    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds the 5MB limit.")
    file_name =file.filename
    student_id = user['student_id']
    return  await StudentCrud(db=db).upload_files_and_images(file_bytes=file_bytes, file_name=file_name, question=question, student_id=student_id)


@router.get('/get-answer/{id}')
async def get_answer( 
    id: str,
     db:db,
    user : current_user,

):
    id = user['student_id']
    return await StudentCrud(db=db).pull_answer(id)

# Resume upload and retrieval

@router.post('/upload-resume/{student_id}')
async def create_file_response(
    file: UploadFile,
    user : current_user,
    student_id: str,
     db:db,
): 
    student_id = user['student_id']
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds the 5MB limit.")
    file_name = file.filename
    return await StudentCrud(db=db).upload_resume_to_ai(file_bytes=contents, file_name=file_name,student_id=student_id)

@router.get('/get-resume/{id}')
async def get_resume(
    id: str,
     db:db,
    user : current_user,
):
    id = user['student_id']
    return await StudentCrud(db=db).pull_resume(id)

# Image generation and retrieval

@router.post('/image-gen/{student_id}')
async def create_image(
    student_id:str,
     db:db,
    user : current_user,
    prompt: str = Form(...),
):
    student_id = user['student_id']
    return await StudentCrud(db=db).flowchart_generation(student_id=student_id,prompt=prompt)

@router.get('/get-image/{id}')
async def get_image(
    id: str,
     db:db,
    user : current_user,
):
    id = user['student_id']
    return await StudentCrud(db=db).pull_flowchart(id)


# Roadmap generation and retrieval

@router.post('/roadmap-gen/{student_id}')
async def create_roadmap( 
    student_id:str,
     db:db,
    user : current_user,
    prompt: str = Form(...),
):
    student_id = user['student_id']
    return await StudentCrud(db=db).roadmap_generation(prompt=prompt,student_id=student_id)

@router.get('/get-roadmap/{id}')
async def get_roadmap( 
    id: str, 
     db:db,
    user : current_user,
):
    id = user['student_id']
    return await StudentCrud(db=db).pull_roadmap(id)


# Image understanding and retrival

@router.post('/image-understand')
async def image_understanding(
    image:UploadFile,
    student_id:str,
     db:db,
    user : current_user,
    question:str = Form(...),
):
    student_id = user['student_id']
    image_byte = await image.read()
    if len(image_byte)  > 5 * 1024 * 1024:
        raise HTTPException(status_code= 400 ,  detail="File size exceeds the 5MB limit.")
    image_name = image.filename
    return await StudentCrud(db=db).image_understandings(student_id=student_id,image_byte=image_byte,question=question,image_name=image_name)


# this is a students activity routes...................................>

@router.get("/task")
async def pull_students_task(
     db:db,
     user:current_user
):
    student_id = user["student_id"]
    return await StudentActivity(db=db).get_students_task(student_id=student_id)


@router.get("/task/{task_id}")
async def pull_students_task(
     db:db,
     task_id:str,
     user:current_user
):
    student_id = user["student_id"]
    return await StudentActivity(db=db).get_students_task_details(student_id=student_id,task_id=task_id)


@router.get("/task/{task_id}/submit")
async def pull_students_task(
     db:db,
     task_id:str,
     user:current_user,
     submission_link: str =Form(...)
):
    student_id = user["student_id"]
    return await StudentActivity(db=db).submit_the_task(task_id=task_id,student_id=student_id,submission_link=submission_link)