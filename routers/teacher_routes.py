from fastapi import APIRouter,UploadFile,Form,Depends
from configs.pgdb import get_db
from crud.teachers import TeacherCrud
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    tags=["Teacher crud"]
)

@router.post('/pdf-understanding')
async def create_file_uploadresponse(
    file: UploadFile, 
    question: str = Form(...), 
    db: AsyncSession= Depends(get_db)
):
    file_bytes= await file.read()
    file_name =file.filename
    return TeacherCrud(db=db).upload_file_docs( file_bytes,file_name, question)


@router.post('/image-understanding')
async def create_imageresponse(
    image:UploadFile,
    question:str = Form(...),
    db:AsyncSession = Depends(get_db)
):
    image_byte = await image.read()
    image_name = image.filename
    
    return TeacherCrud(db=db).upload_image(image_byte,image_name,question)

