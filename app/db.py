from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

ASYNC_DB_URL = "mysql+aiomysql://root:password@db:3306/circle_development?charset=utf8"

async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session

# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from env import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

# DATABASE = "mysql://%s:%s@%s/%s?charset=utf8" % (
#     DB_USER,
#     DB_PASSWORD,
#     DB_HOST,
#     DB_NAME,
# )

# engine = create_engine(DATABASE, encoding="utf-8", echo=True)

# Base = declarative_base()