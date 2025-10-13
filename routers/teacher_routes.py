from fastapi import APIRouter,UploadFile,Form,Depends
from configs.pgdb import get_db
from Controlers.teachers import TeacherCrud
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    tags=["Teacher crud"]
)

@router.post('/pdf-understanding/{teacher_id}')
async def create_file_uploadresponse(teacher_id: str ,file: UploadFile, question: str = Form(...), db: AsyncSession= Depends(get_db)):
    file_bytes= await file.read()
    file_name =file.filename
    return await TeacherCrud(db=db).upload_file_docs( teacher_id=teacher_id,file_bytes=file_bytes,file_name=file_name,question= question)


@router.post('/image-understanding/{teacher_id}')
async def create_imageresponse(teacher_id: str ,image:UploadFile,question:str = Form(...),db:AsyncSession = Depends(get_db)):
    image_byte = await image.read()
    image_name = image.filename
    return await TeacherCrud(db=db).upload_image(teacher_id=teacher_id,image_byte=image_byte,image_name=image_name,question=question)

@router.get('/get-pdf-response/{id}')
async def get_pdf_response(id:str,db:AsyncSession = Depends(get_db)):
    return await TeacherCrud(db=db).pull_file(id)

@router.get('/get-image-response/{id}')
async def get_image_response(id:str,db:AsyncSession = Depends(get_db)):
    return await TeacherCrud(db=db).pull_image(id)