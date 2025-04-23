from sqlalchemy import create_engine
from sqlalchemy.orm import Session


# 接続先DBの設定
DATABASE = "sqlite:///db.sqlite3"

# Engine の作成
engine = create_engine(DATABASE, echo=False)

# Sessionの作成
session = Session(autocommit=False, autoflush=False, bind=engine)
