# from sqlalchemy import create_engine

# from app.models.task import Base
# from app.models.task2 import Base


# DB_URL = "mysql+pymysql://root:password@db:3306/circle_development?charset=utf8"
# engine = create_engine(DB_URL, echo=True)


# def reset_database():
#     Base.metadata.drop_all(bind=engine)
#     # Base.metadata.create_all(bind=engine)


# if __name__ == "__main__":
#     reset_database()