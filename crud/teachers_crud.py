from fastapi import HTTPException
from sqlalchemy import select,func,update
from sqlalchemy.ext.asyncio import AsyncSession
from models.teacher_models import Task,TaskAssignment
from utils.uniqueid import create_unique_id
from icecream import ic
from datetime import datetime,timezone

class __TeacherCrud:
    def __init__(self,db:AsyncSession):
        self.db = db
        self.task = Task
        self.task_assign = TaskAssignment
class TeacherActivities(__TeacherCrud):

    async def assign_task(self, title, describtion, due_date, teacher_id, student_ids):
        
        ic(student_ids)
        ic(teacher_id)
        try:
            async with self.db.begin():
                add_task = self.task(
                    id = create_unique_id(title),
                    title=title,
                    describtion=describtion,
                    due_date=due_date,
                    teacher_id=teacher_id,
                    assigned_at = datetime.now(timezone.utc)
                )
                self.db.add(add_task)
                

                for student_id in student_ids:
                    task_for_students = self.task_assign(
                        id = create_unique_id(student_id),
                        task_id=add_task.id,
                        student_id=student_id
                    )
                    self.db.add(task_for_students)

                return {
                    "message": "Task Added Successfully!",
                    "task_id": add_task.id,
                    "assigned_to": student_ids
                }

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Something went wrong while adding task: {e}")

   

    # async def assign_task(self, title, describtion, due_date, teacher_id, student_ids):
    # from icecream import ic
    # ic(student_ids)
    # ic(teacher_id)
    # try:
    #     # Wrap everything in a single transaction
    #     async with self.db.begin():
    #         # Add task
    #         add_task = self.task(
    #             id=create_unique_id(title),
    #             title=title,
    #             describtion=describtion,
    #             due_date=due_date,
    #             teacher_id=teacher_id
    #         )
    #         self.db.add(add_task)
    #         await self.db.flush()  # ensures add_task.id is available

    #         # Add assignments
    #         for student_id in student_ids:
    #             task_for_students = self.task_assign(
    #                 task_id=add_task.id,
    #                 student_id=student_id
    #             )
    #             self.db.add(task_for_students)

    #     # No need to call await self.db.commit(), the async context commits automatically

    #     return {
    #         "message": "Task Added Successfully!",
    #         "task_id": add_task.id,
    #         "assigned_to": student_ids
    #     }

    # except HTTPException:
    #     raise
    # except Exception as e:
    #     # rollback is automatic on exception in async with
    #     raise HTTPException(status_code=500, detail=f"Something went wrong while adding task: {e}")
