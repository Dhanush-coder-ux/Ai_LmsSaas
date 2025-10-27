from crud.teachers_crud import( HTTPException,AsyncSession,TaskAssignment,Task)
from sqlalchemy import func,select,update
from models.students_models import StudentActivitys
from utils.uniqueid import create_unique_id
from icecream import ic


class __StudentCrud:
    def __init__(self,db:AsyncSession):
        self.db = db
        self.activity = StudentActivitys

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

            raise HTTPException(status_code=500,detail=f"something went wrong while geting  all task {e}")
        
        
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
        async with self.db.begin():
            assignment = update(TaskAssignment).where(
                TaskAssignment.task_id == task_id,
                TaskAssignment.student_id == student_id
            ).values(
                submission_link = submission_link,
                is_completed = True,
            ).returning(TaskAssignment.task_id)

            is_updated = (await self.db.execute(assignment)).scalar_one_or_none()

            if not is_updated:
                raise HTTPException(status_code=404,detail="Task not found or not assigned you !")

            return {
                "message": " Task submitted successfully!", 
                "submission_link": submission_link
                }
    
    async def save_activity(self,student_id,topic,duration,accuracy):
        ic(student_id,topic,duration,accuracy)
        
        try:
            activity = self.activity(
            id = create_unique_id('quize_data'),
            student_id = student_id,
            topic =   topic,
            duration = duration,
            accuracy = accuracy
            )
            ic(activity)
            self.db.add(activity)
            await self.db.commit()
            return {'message' : "Activity saved successfully !"}
        except HTTPException :
            raise
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"something went wrong while saving activity{e}")
        
    async def get_student_analytics(self, student_id):
        ic("hello from get_student_analytics",student_id)
        try:
            result = (
                await self.db.execute(
                    select(
                        self.activity.topic,
                        func.avg(self.activity.accuracy).label("avg_accuracy"),
                        func.sum(self.activity.duration).label("total_time")
                    )
                    .where(self.activity.student_id == student_id)
                    .group_by(self.activity.topic)
                )
            ).mappings().all()

            ic(result)

            analytics = [
                {
                    "topic": r["topic"],
                    "avg_accuracy": float(r["avg_accuracy"] or 0),
                    "total_time": int(r["total_time"] or 0)
                }
                for r in result
            ]
            ic(analytics)
            return analytics

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get analytics: {e}")

    
