from fastapi import HTTPException
from sqlalchemy import select,func
from sqlalchemy.ext.asyncio import AsyncSession
from models.teacher_models import Task,TaskAssignment
from utils.uniqueid import create_unique_id


class __TeacherCrud:
    def __init__(self,db:AsyncSession):
        self.db = db
        self.task = Task
        self.task_assign = TaskAssignment
class TeacherActivities(__TeacherCrud):

    async def assign_task(self, title, describtion, due_date, teacher_id, student_ids):
        try:
            add_task = self.task(
                id = create_unique_id(title),
                title=title,
                describtion=describtion,
                due_date=due_date,
                teacher_id=teacher_id
            )
            self.db.add(add_task)
            await self.db.commit()
            await self.db.refresh(add_task)

            for student_id in student_ids:
                task_for_students = self.task_assign(
                    task_id=add_task.id,
                    student_id=student_id
                )
                self.db.add(task_for_students)

            await self.db.commit()

            return {
                "message": "Task Added Successfully!",
                "task_id": add_task.id,
                "assigned_to": student_ids
            }

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Something went wrong while adding task: {e}")

   

        