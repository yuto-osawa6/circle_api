from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

ASYNC_DB_URL = "mysql+aiomysql://root:password@db:3306/circle_development?charset=utf8"

async_engine = create_async_engine(ASYNC_DB_URL, echo=True, pool_pre_ping=True)  # このオプションを有効にする)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

Base = declarative_base()


# async def get_db():
#     async with async_session() as session:
#         yield session
        # await session.execute(stmt)
async def get_db():
    async with async_session() as session:
        # async with session.begin():
            yield session