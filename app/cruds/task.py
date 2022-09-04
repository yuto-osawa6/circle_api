from sqlalchemy.ext.asyncio import AsyncSession

import app.models.task as task_model
import app.schemas.task as task_schema

from typing import List, Tuple, Optional

from sqlalchemy import select
from sqlalchemy.engine import Result

async def create_task(
    db: AsyncSession, task_create: task_schema.TaskCreate
) -> task_model.Task:
    task = task_model.Task(**task_create.dict())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get_tasks_with_done(db: AsyncSession):
# async def get_tasks_with_done(db: AsyncSession) -> List[Optional[task_model.Done]]:

    result: Result = await (
        db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
                # task_model.Task.title2,
                task_model.Done.id.isnot(None).label("done"),
            ).outerjoin(task_model.Done)
        )
    )

    result2: Result = await (
        db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
                task_model.Done.id.isnot(None).label("done"),
            ).outerjoin(task_model.Done)
        )
    )
    # print("aaaaa")

    # print()
    return {"data":result.all(),"status":200}
    # return result.all()


async def get_task(db: AsyncSession, task_id: int) -> Optional[task_model.Task]:
    result: Result = await db.execute(
        select(task_model.Task).filter(task_model.Task.id == task_id)
    )
    task: Optional[Tuple[task_model.Task]] = result.first()
    # print(task)
    return task[0] if task is not None else None  # 要素が一つであってもtupleで返却されるので１つ目の要素を取り出す


async def update_task(
    db: AsyncSession, task_create: task_schema.TaskCreate, original: task_model.Task
) -> task_model.Task:
    original.title = task_create.title
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original
