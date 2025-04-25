from config import settings
from sqlmodel import create_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, sessionmaker
from sqlalchemy_utils import create_database, database_exists
from typing import Annotated

engine = create_engine(settings.db_url, echo=True)

pk = Annotated[int, mapped_column(primary_key=True)]

class Base(DeclarativeBase):
    __abstract__ = True

def init_database():
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)