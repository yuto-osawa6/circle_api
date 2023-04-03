from sqlalchemy.ext.asyncio import AsyncSession

import app.models.task as task_model
import app.models.user as user_model

import app.schemas.task as task_schema
import app.schemas.user as user_schema


from typing import List, Tuple, Optional

from sqlalchemy import select
from sqlalchemy.engine import Result
import random
import string
import itertools
import uuid

def sample(**args):
    print(args)
# sample(name='Tom', age='25', gender='male') # {'name': 'Tom', 'age': '25', 'gender': 'male'}
def get_random_str(num):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num))

async def ota(
    db: AsyncSession,
    # user_create: user_schema.UserCreate,
    task_create: task_schema.TaskCreate
) -> task_model.Task:
    # print("aaa")
    print(task_create)
    print(task_create.dict())
    print(*task_create.dict())
    print(*task_create)

    # icd_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
    #             'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
    #             '1','2','3','4','5','6','7','8','9','10'
    # ]


    # icd = random.choices(icd_list, k=10)
    # print(icd)
    comb = itertools.combinations(string.ascii_letters + string.digits, 1)
    print(len(list(comb)))

    get_random_str(8)
      # print(**task_create)
      # a = [name='Tom', age='25', gender='male']
      # print(a.dict())

    # print(f"{**task_create.dict()}")
    # print("aaa")
    # task = task_model.Task(title='クリーニングを取りに行く',title2='クリーニングを取りに行く2')
    # db.add(task)
    # await db.commit()
    # await db.refresh(task)

    # result: Result = await db.execute(
    #     select(task_model.Task).filter(task_model.Task.id == 1)
    # )
    # task: Optional[Tuple[task_model.Task]] = result.first()

    # result: Result = await db.execute(
    #     select(user_model.User).filter(
    #         user_model.User.uid == 1,
    #         user_model.User.email == "atgmw628@gmail.com"
    #         )
    #     )
    # user: Optional[Tuple[user_model.User]] = result.first()

    # print(user)
    
    # print(user[0] if user is not None else None)
    # if user == None:
      # print("No")
    #   a = "aaa"
    #   # print(user_create)
    #   pass
    # print(a)
    # print(task[0])
    # return task[0]
  
# -----------------------------

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
    # result[1]

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
