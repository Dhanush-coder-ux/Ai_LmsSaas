from crud.teachers_crud import select,HTTPException,AsyncSession,TaskAssignment,Task
from datetime import datetime,timezone


class __StudentCrud:
    def __init__(self,db:AsyncSession):
        self.db = db
class StudentActivity(__StudentCrud):
    
    async def get_students_task(self,student_id):
        try:
            task = (await self.db.execute(
                select(TaskAssignment)
                .join(Task)
                .where(TaskAssignment.student_id == student_id)
                .order_by(Task.due_date.asc())
            )).scalars().all()

            if not task:
                raise HTTPException(status_code=404,detail="Task Not Found !")
            return task
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"something went wrong while geting  all task")
        
    async def get_students_task_details(self,student_id,task_id):
        try:
            task = (await self.db.execute(
                select(TaskAssignment)
                .join(Task)
                .where(
                    TaskAssignment.task_id == task_id,
                    TaskAssignment.student_id == student_id
                    )
            )).scalar_one_or_none()

            if not task:
                raise HTTPException(status_code=404,detail="Task Not Found !")
            return task
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"something went wrong while geting  all task {e}")
        
    async def submit_the_task(self ,task_id, student_id, submission_link ):
        assignment =( await self.db.execute(
            select(TaskAssignment)
            .where(
                TaskAssignment.task_id == task_id,
                TaskAssignment.student_id == student_id
            )
        )).scalar_one_or_none()

        if not assignment:
            raise HTTPException(status_code=404,detail="Task not found or not assigned you !")
        
        assignment.submission_link = submission_link
        assignment.is_completed = True
        assignment.assigned_at = datetime.now(tz=timezone.utc)
        await self.db.commit()

        return {"message": " Task submitted successfully!", "submission_link": submission_link}
        