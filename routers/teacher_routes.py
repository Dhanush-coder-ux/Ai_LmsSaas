from fastapi import APIRouter,UploadFile,Form,Depends,HTTPException
from configs.pgdb import get_db
from Controlers.teachers import TeacherCrud
from crud.teachers_crud import TeacherActivities
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated,List
from security.token_verify import get_current_user
from schemas.teacher_task import AssignTaskSchema




router = APIRouter(
    tags=["Teacher crud"]
)

db = Annotated[AsyncSession ,Depends(get_db)]
current_user = Annotated[dict,Depends(get_current_user)]



# techers ai access routes .....................................>

@router.post('/pdf-understanding/{teacher_id}')
async def create_file_uploadresponse(
    user:current_user,
    db: db,
    file: UploadFile,
    question: str = Form(...), 
  
):
    teacher_id = user['user_id']
    file_bytes= await file.read()
    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds the 5MB limit.")
    file_name =file.filename
    return await TeacherCrud(db=db).upload_file_docs( 
        teacher_id=teacher_id,
        file_bytes=file_bytes,
        file_name=file_name,
        question= question
)


@router.post('/image-understanding/{teacher_id}')
async def create_imageresponse(
     user:current_user, 
    image:UploadFile,
    db:db,
    question:str = Form(...),
):
    teacher_id = user['user_id']
    image_byte = await image.read()
    if len(image_byte) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image size exceeds the 5MB limit.")
    image_name = image.filename
    return await TeacherCrud(db=db).upload_image(
        teacher_id=teacher_id,
        image_byte=image_byte,
        image_name=image_name,
        question=question
)


@router.post('/question-paper')
async def create_question_paper(
     user:current_user,
     db:db,
    file:UploadFile,
    question:str = Form(...),
):
    teacher_id = user['user_id']
    file_bytes = await file.read()
    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds the 5MB limit.")
    file_name = file.filename
    return await TeacherCrud(db=db).get_question_from_ai(
        teacher_id=teacher_id,
        file_bytes=file_bytes,
        file_name=file_name,
        question=question
)


@router.get('/get-pdf-response/{id}')
async def get_pdf_response( user:current_user, db:db,):
    teacher_id = user['user_id']
    return await TeacherCrud(db=db).pull_file(teacher_id=teacher_id)

@router.get('/get-image-response/{id}')
async def get_image_response( user:current_user, db:db,):
    teacher_id = user['user_id']
    return await TeacherCrud(db=db).pull_image(id)

@router.get('/question-paper')
async def get_question_paper( user:current_user, db:db,):
    teacher_id = user['user_id']
    return await TeacherCrud(db=db).pull_question_paper(teacher_id=id)



# teachers activity routes.................................................>

@router.post('/assign-task')
async def create_task(
    user:current_user,
    db:db,
   request:AssignTaskSchema,  
):
    teacher_id = user['user_id']
    from icecream import ic
    ic(teacher_id)
    return await TeacherActivities(db=db).assign_task(
    student_ids=request.student_ids,
        teacher_id=teacher_id,
        title=request.title,
        describtion=request.description,
        due_date=request.due_date
)

