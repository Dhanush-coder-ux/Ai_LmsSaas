from fastapi import APIRouter,UploadFile,Form,Depends,HTTPException
from configs.pgdb import get_db
from Controlers.teachers import TeacherCrud
from crud.teachers_crud import TeacherActivities
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated,List



db = Annotated[AsyncSession ,Depends(get_db)]


router = APIRouter(
    tags=["Teacher crud"]
)

# techers ai access routes .....................................>

@router.post('/pdf-understanding/{teacher_id}')
async def create_file_uploadresponse(
    teacher_id: str ,
    db: db,
    file: UploadFile,
    question: str = Form(...), 
  
):
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
    teacher_id: str ,
    image:UploadFile,
    db:db,
    question:str = Form(...),
):
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
    teacher_id:str,
     db:db,
    file:UploadFile,
    question:str = Form(...),
):
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
async def get_pdf_response(id:str, db:db,):
    return await TeacherCrud(db=db).pull_file(id)

@router.get('/get-image-response/{id}')
async def get_image_response(id:str, db:db,):
    return await TeacherCrud(db=db).pull_image(id)

@router.get('/question-paper')
async def get_question_paper(id : str, db:db,):
    return await TeacherCrud(db=db).pull_question_paper(teacher_id=id)



# teachers activity routes.................................................>

@router.post('/assign-task')
async def create_task(
    teacher_id : str,
    db:db,
    student_id:List[str] = Form(...),
    title: str = Form(...),
    description : str = Form(...),
    due_date : str = Form(),
    
    
):
    return await TeacherActivities(db=db).assign_task(
        student_ids=student_id,
        teacher_id=teacher_id,
        title=title,
        description=description,
        due_date=due_date,

)

