# from sqlalchemy import create_engine, Table, MetaData


# def versions():
#   metadata = MetaData(bind=engine)
#   alembic_version = Table('alembic_version', metadata, autoload=True)

#   # alembic_versionテーブルから全てのレコードを取得
#   select_stmt = alembic_version.select()
#   result = engine.execute(select_stmt)
#   # レコードを出力
#   for row in result:
#       print(row)


def samples():
  print("aaa")

