from typing import Iterable

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from src.config import Env

env = Env()

engine = create_engine(
    env.connection_string, connect_args={"options": "-c timezone=utc"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def import_dependency_models() -> None:
    from src import models  # noqa: F401


def get_db() -> Iterable[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db() -> None:
    from sqlalchemy_utils.functions import create_database

    create_database(env.connection_string)
    Base.metadata.create_all(engine)


def drop_db() -> None:
    from sqlalchemy_utils.functions import database_exists, drop_database

    if database_exists(env.connection_string):
        drop_database(env.connection_string)


# SqlAlchemyのモデルをインポートしないと、テーブル作成時に認識漏れするため、インポートしておく
import_dependency_models()
